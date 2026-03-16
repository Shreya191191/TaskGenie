package com.aishreya.taskgenie.data.reminder

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "reminders")
data class ReminderEntity(

    @PrimaryKey(autoGenerate = true)
    val id: Int = 0,

    val message: String,

    val triggerTime: Long
)