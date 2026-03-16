package com.aishreya.taskgenie.agent

import java.text.SimpleDateFormat
import java.util.*

data class ParsedReminder(
    val message: String,
    val triggerTime: Long
)

object NLPDateTimeParser {

    fun parse(input: String): ParsedReminder? {

        val text = input.lowercase()
        val calendar = Calendar.getInstance()


        // -------------------------
       // in X seconds
       // -------------------------
        Regex("in (\\d+) seconds").find(text)?.let {
            val sec = it.groupValues[1].toInt()
            calendar.add(Calendar.SECOND, sec)
            return ParsedReminder(extractTask(text), calendar.timeInMillis)
        }


        // -------------------------
        // in X minutes
        // -------------------------
        Regex("in (\\d+) minutes").find(text)?.let {
            val min = it.groupValues[1].toInt()
            calendar.add(Calendar.MINUTE, min)
            return ParsedReminder(extractTask(text), calendar.timeInMillis)
        }

        // -------------------------
        // after X hours
        // -------------------------
        Regex("after (\\d+) hours").find(text)?.let {
            val hr = it.groupValues[1].toInt()
            calendar.add(Calendar.HOUR_OF_DAY, hr)
            return ParsedReminder(extractTask(text), calendar.timeInMillis)
        }

        // -------------------------
        // after X days
        // -------------------------
        Regex("(\\d+) days").find(text)?.let {
            val days = it.groupValues[1].toInt()
            calendar.add(Calendar.DAY_OF_YEAR, days)
        }

        // -------------------------
        // after X years
        // -------------------------
        Regex("(\\d+) years").find(text)?.let {
            val years = it.groupValues[1].toInt()
            calendar.add(Calendar.YEAR, years)
        }

        // -------------------------
        // tomorrow
        // -------------------------
        if (text.contains("tomorrow")) {
            calendar.add(Calendar.DAY_OF_YEAR, 1)
        }

        // -------------------------
        // weekday support
        // -------------------------
        val daysMap = mapOf(
            "monday" to Calendar.MONDAY,
            "tuesday" to Calendar.TUESDAY,
            "wednesday" to Calendar.WEDNESDAY,
            "thursday" to Calendar.THURSDAY,
            "friday" to Calendar.FRIDAY,
            "saturday" to Calendar.SATURDAY,
            "sunday" to Calendar.SUNDAY
        )

        daysMap.forEach { (name, day) ->
            if (text.contains(name)) {
                val today = calendar.get(Calendar.DAY_OF_WEEK)
                var diff = day - today
                if (diff <= 0) diff += 7
                calendar.add(Calendar.DAY_OF_YEAR, diff)
            }
        }

        // -------------------------
        // time detection
        // -------------------------
        val timeRegex = Regex("(\\d{1,2})(:(\\d{2}))?\\s*(am|pm)")
        val match = timeRegex.find(text)

        if (match != null) {

            var hour = match.groupValues[1].toInt()
            val minute =
                if (match.groupValues[3].isNotEmpty())
                    match.groupValues[3].toInt()
                else
                    0

            val ampm = match.groupValues[4]

            if (ampm == "pm" && hour != 12) hour += 12
            if (ampm == "am" && hour == 12) hour = 0

            calendar.set(Calendar.HOUR_OF_DAY, hour)
            calendar.set(Calendar.MINUTE, minute)
            calendar.set(Calendar.SECOND, 0)

        }

        return ParsedReminder(
            extractTask(text),
            calendar.timeInMillis
        )
    }

    private fun extractTask(text: String): String {

        return text.substringAfter("to", "Reminder").trim()
    }
}