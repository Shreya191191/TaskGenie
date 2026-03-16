package com.aishreya.taskgenie.tools.reminder

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.util.Log
import com.aishreya.taskgenie.data.reminder.ReminderDatabase
import com.aishreya.taskgenie.ui.alarm.AlarmActivity
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch

class ReminderReceiver : BroadcastReceiver() {

    override fun onReceive(context: Context, intent: Intent) {

        Log.d("REMINDER_DEBUG", "ReminderReceiver triggered")

        val message = intent.getStringExtra("message") ?: "Reminder"
        val id = intent.getIntExtra("reminderId", -1)

        // 🔔 Open alarm screen
        val alarmIntent = Intent(context, AlarmActivity::class.java)
        alarmIntent.putExtra("message", message)
        alarmIntent.flags = Intent.FLAG_ACTIVITY_NEW_TASK
        context.startActivity(alarmIntent)

        // 🔥 DB से reminder delete
        val db = ReminderDatabase.getDatabase(context)
        val dao = db.reminderDao()

        CoroutineScope(Dispatchers.IO).launch {
            if (id != -1) {
                dao.deleteReminder(id)
            }
        }
    }
}