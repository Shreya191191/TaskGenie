package com.aishreya.taskgenie.agent

import android.content.Context
import android.util.Log
import com.aishreya.taskgenie.data.MCPClient
import com.aishreya.taskgenie.agent.NLPDateTimeParser
import com.aishreya.taskgenie.data.model.GeminiClient
import com.aishreya.taskgenie.tools.reminder.ReminderTool

class AIAgent {

    private val gemini = GeminiClient()
    private val client = MCPClient()

    suspend fun processMessage(context:Context, message: String): String {

        Log.d("AI_AGENT", "User message: $message")

        return try {

            val aiResponse = gemini.analyzeIntent(message)

            Log.d("AI_AGENT", "Gemini response: $aiResponse")

            when {

                aiResponse.contains("weather") -> {

                    val city = extractValue(aiResponse, "city")

                    if (city.isEmpty()) {
                        "Please tell the city name."
                    } else {
                        client.getWeather(city)
                    }
                }

                aiResponse.contains("mail") -> {

                    val email = extractValue(aiResponse, "email")
                    val msg = extractValue(aiResponse, "message")

                    if (email.isEmpty() || msg.isEmpty()) {
                        "I couldn't understand the email format."
                    } else {
                        client.sendMail(context, email, msg)
                    }
                }

                aiResponse.contains("reminder") -> {

                    val parsed = NLPDateTimeParser.parse(message)

                    if (parsed != null) {

                        ReminderTool.setReminder(
                            context,
                            parsed.message,
                            parsed.triggerTime
                        )

                        "Reminder set successfully 👍"

                    } else {
                        "Couldn't understand the reminder time."
                    }
                }

                else -> {

                    "Sorry, I couldn't understand your request."
                }
            }

        } catch (e: Exception) {

            Log.e("AI_AGENT", "Error: ${e.message}")

            "Something went wrong."
        }
    }
    private fun extractValue(json: String, key: String): String {

        val regex = Regex("\"$key\"\\s*:\\s*\"(.*?)\"")

        return regex.find(json)?.groupValues?.get(1) ?: ""
    }
}