package com.aishreya.taskgenie.data.reminder

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.Query

@Dao
interface ReminderDao {

    @Insert
    suspend fun insertReminder(reminder: ReminderEntity)

    @Query("SELECT * FROM reminders")
    suspend fun getAllReminders(): List<ReminderEntity>

    @Query("DELETE FROM reminders WHERE id = :id")
    suspend fun deleteReminder(id: Int)

}