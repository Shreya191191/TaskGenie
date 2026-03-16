package com.aishreya.taskgenie.ui.alarm

import android.app.Activity
import android.app.AlarmManager
import android.app.PendingIntent
import android.content.Intent
import android.media.MediaPlayer
import android.os.Bundle
import android.os.Handler
import android.provider.Settings
import android.speech.tts.TextToSpeech
import android.view.WindowManager
import android.widget.Button
import com.aishreya.taskgenie.R
import com.aishreya.taskgenie.tools.reminder.ReminderReceiver
import com.google.android.gms.auth.api.signin.GoogleSignIn
import java.util.*

class AlarmActivity : Activity(), TextToSpeech.OnInitListener {

    private lateinit var player: MediaPlayer
    private lateinit var tts: TextToSpeech
    private val handler = Handler()

    private var message: String = "Reminder"
    private var userName: String = "User"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // 🔒 lock screen + turn screen on
        window.addFlags(
            WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON or
                    WindowManager.LayoutParams.FLAG_TURN_SCREEN_ON or
                    WindowManager.LayoutParams.FLAG_SHOW_WHEN_LOCKED
        )

        setContentView(R.layout.activity_alarm)

        message = intent.getStringExtra("message") ?: "Reminder"

        // get Google user name
        val account = GoogleSignIn.getLastSignedInAccount(this)
        userName = account?.displayName ?: "User"

        // 🔔 alarm sound
        player = MediaPlayer.create(this, Settings.System.DEFAULT_ALARM_ALERT_URI)
        player.isLooping = true
        player.start()

        // 🗣 TTS init
        tts = TextToSpeech(this, this)

        // 🛑 stop button
        findViewById<Button>(R.id.stopBtn).setOnClickListener {
            stopAlarm()
        }

        // 😴 snooze button
        findViewById<Button>(R.id.snoozeBtn).setOnClickListener {

            val snoozeTime = System.currentTimeMillis() + 5 * 60 * 1000

            val intent = Intent(this, ReminderReceiver::class.java)
            intent.putExtra("message", message)

            val pendingIntent = PendingIntent.getBroadcast(
                this,
                1,
                intent,
                PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
            )

            val alarmManager = getSystemService(ALARM_SERVICE) as AlarmManager

            alarmManager.set(
                AlarmManager.RTC_WAKEUP,
                snoozeTime,
                pendingIntent
            )

            stopAlarm()
        }
    }

    override fun onInit(status: Int) {

        if (status == TextToSpeech.SUCCESS) {

            val result = tts.setLanguage(Locale.US)

            if (result != TextToSpeech.LANG_MISSING_DATA &&
                result != TextToSpeech.LANG_NOT_SUPPORTED) {

                startVoiceLoop()
            }
        }
    }

    // 🔊 voice reminder every 15 sec
    private fun startVoiceLoop() {

        val runnable = object : Runnable {
            override fun run() {

                tts.speak(
                    "Hey $userName, it's time to $message",
                    TextToSpeech.QUEUE_FLUSH,
                    null,
                    null
                )

                handler.postDelayed(this, 15000)
            }
        }

        handler.postDelayed(runnable, 1500)
    }

    private fun stopAlarm() {

        handler.removeCallbacksAndMessages(null)

        if (::player.isInitialized) {
            player.stop()
            player.release()
        }

        finish()
    }

    override fun onDestroy() {
        super.onDestroy()

        if (::tts.isInitialized) {
            tts.shutdown()
        }
    }
}