package com.aishreya.taskgenie.ui.reminder

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.ArrayAdapter
import android.widget.ListView
import androidx.lifecycle.lifecycleScope
import com.aishreya.taskgenie.R
import com.aishreya.taskgenie.data.reminder.ReminderDatabase
import kotlinx.coroutines.launch

class ReminderListActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContentView(R.layout.activity_reminder_list)

        val listView = findViewById<ListView>(R.id.reminderList)

        val db = ReminderDatabase.getDatabase(this)

        lifecycleScope.launch {

            val reminders = db.reminderDao().getAllReminders()

            val messages = reminders.map { it.message }

            val adapter = ArrayAdapter(
                this@ReminderListActivity,
                android.R.layout.simple_list_item_1,
                messages
            )

            listView.adapter = adapter
        }
    }
}