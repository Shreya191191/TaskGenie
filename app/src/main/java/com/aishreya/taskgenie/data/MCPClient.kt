package com.aishreya.taskgenie.data


import android.content.Context
import android.content.Intent
import android.net.Uri
import com.aishreya.taskgenie.tools.gmail.EmailSender
import com.aishreya.taskgenie.tools.gmail.GmailServiceHelper
import com.aishreya.taskgenie.tools.weather.RetrofitInstance
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

class MCPClient {

    suspend fun getWeather(city: String): String {

        return try {

            val response =
                RetrofitInstance.api.getWeather(
                    city,
                    "7aa8f4969101dbe4e86c3c76d3b588b9"
                )

            val temp = response.main.temp
            val humidity = response.main.humidity
            val desc = response.weather[0].description

            """
            Weather in $city
            Temp: $temp °C
            Humidity: $humidity%
            Condition: $desc
            """.trimIndent()

        } catch (e: Exception) {
            "Error getting weather"
        }
    }

    suspend fun sendMail(
        context: Context,
        email: String,
        msg: String
    ): String {

        return withContext(Dispatchers.IO) {

            try {

                val gmailService =
                    GmailServiceHelper.getService(context)

                EmailSender.sendEmail(
                    gmailService,
                    email,
                    "AI Agent Message",
                    msg
                )

                "Email sent to $email"

            } catch (e: Exception) {

                "Mail failed: ${e.message}"
            }
        }
    }
}