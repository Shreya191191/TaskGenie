package com.aishreya.taskgenie.tools.gmail


import android.util.Base64
import com.google.api.services.gmail.Gmail
import com.google.api.services.gmail.model.Message
import java.io.ByteArrayOutputStream
import java.util.Properties
import javax.mail.Session
import javax.mail.internet.InternetAddress
import javax.mail.internet.MimeMessage

object EmailSender {

    fun sendEmail(
        service: Gmail,
        to: String,
        subject: String,
        body: String
    ) {

        val props = Properties()
        val session = Session.getDefaultInstance(props, null)

        val email = MimeMessage(session)

        email.setFrom(InternetAddress("me"))
        email.addRecipient(
            javax.mail.Message.RecipientType.TO,
            InternetAddress(to)
        )

        email.subject = subject
        email.setText(body)

        val buffer = ByteArrayOutputStream()
        email.writeTo(buffer)

        val raw = Base64.encodeToString(
            buffer.toByteArray(),
            Base64.URL_SAFE or Base64.NO_WRAP
        )

        val message = Message()
        message.raw = raw

        service.users().messages()
            .send("me", message)
            .execute()
    }

}
