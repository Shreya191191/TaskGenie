package com.aishreya.taskgenie.agent

import android.content.Context
import android.util.Log
import com.aishreya.taskgenie.data.MCPClient

class AIAgent {

    private val client = MCPClient()

    suspend fun processMessage(context:Context, message: String): String {

        val text = message.lowercase()
        Log.d("AI_AGENT", "Message received: $message")
        return when {

            text.startsWith("weather") -> {

                val city = message.replace("weather", "").trim()

                client.getWeather(city)
            }

            text.startsWith("mail") -> {

                val parts = message.split(",")

                if (parts.size < 3) {
                    "Format: mail,email,message"
                } else {

                    val email = parts[1].trim()
                    val msg = parts[2].trim()

                    client.sendMail(context, email, msg)
                }
            }

            else -> {

                """
                Try commands:
                
                weather Delhi
                
                mail,abc@gmail.com,Hello bro
                """.trimIndent()
            }
        }
    }
}