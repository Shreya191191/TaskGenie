package com.aishreya.taskgenie.tools.reminder

import android.app.AlarmManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.util.Log
import com.aishreya.taskgenie.data.reminder.ReminderDatabase
import com.aishreya.taskgenie.data.reminder.ReminderEntity
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch

object ReminderTool {

    fun setReminder(
        context: Context,
        message: String,
        triggerTime: Long
    ) {

        val reminderId = (System.currentTimeMillis() % Int.MAX_VALUE).toInt()

        // 📌 SAVE REMINDER TO ROOM DATABASE
        val db = ReminderDatabase.getDatabase(context)
        val dao = db.reminderDao()

        CoroutineScope(Dispatchers.IO).launch {

            dao.insertReminder(
                ReminderEntity(
                    id = reminderId,
                    message = message,
                    triggerTime = triggerTime
                )
            )
        }

        // 📌 ALARM MANAGER
        val intent = Intent(context, ReminderReceiver::class.java)
        intent.putExtra("message", message)
        intent.putExtra("reminderId", reminderId)


        val pendingIntent = PendingIntent.getBroadcast(
            context,
            reminderId,
            intent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )


        val alarmManager =
            context.getSystemService(Context.ALARM_SERVICE) as AlarmManager
        Log.d("REMINDER_DEBUG", "Alarm scheduled for $triggerTime")

        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.S) {

            if (alarmManager.canScheduleExactAlarms()) {
                alarmManager.setExactAndAllowWhileIdle(
                    AlarmManager.RTC_WAKEUP,
                    triggerTime,
                    pendingIntent
                )
            } else {
                alarmManager.set(
                    AlarmManager.RTC_WAKEUP,
                    triggerTime,
                    pendingIntent
                )
            }

        } else {

            alarmManager.setExactAndAllowWhileIdle(
                AlarmManager.RTC_WAKEUP,
                triggerTime,
                pendingIntent
            )

        }
    }
}