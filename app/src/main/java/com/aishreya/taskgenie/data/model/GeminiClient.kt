package com.aishreya.taskgenie.data.model

import com.aishreya.taskgenie.BuildConfig
import com.google.ai.client.generativeai.GenerativeModel
import com.google.ai.client.generativeai.type.content

class GeminiClient {

    private val model = GenerativeModel(
        modelName = "gemini-1.5-flash",
        apiKey = BuildConfig.GEMINI_API_KEY
    )

    suspend fun analyzeIntent(message: String): String {

        val prompt = """
You are TaskGenie, an intelligent AI assistant.

Your job is to analyze the user message and decide which tool should be used.

TOOLS AVAILABLE:

1. weather
Description: Get current weather information for a city.
Arguments:
{
 "tool": "weather",
 "city": "<city_name>"
}

2. mail
Description: Send an email.
Arguments:
{
 "tool": "mail",
 "email": "<recipient_email>",
 "message": "<email_message>"
}

3. reminder
Description: Set a reminder for the user.
Arguments:
{
 "tool": "reminder",
 "message": "<reminder_message>",
 "time": "<natural_language_time>"
}

RULES:

1. Always respond ONLY with JSON.
2. Do not explain anything.
3. Choose the most appropriate tool.
4. If no tool matches, return:
{
 "tool": "none"
}

User message:
$message
""".trimIndent()

        val response = model.generateContent(
            content { text(prompt) }
        )

        return response.text ?: ""
    }
}