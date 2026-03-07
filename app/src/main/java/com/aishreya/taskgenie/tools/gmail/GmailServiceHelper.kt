package com.aishreya.taskgenie.tools.gmail

import android.content.Context
import android.util.Log
import com.google.android.gms.auth.api.signin.GoogleSignIn
import com.google.api.client.extensions.android.http.AndroidHttp
import com.google.api.client.googleapis.extensions.android.gms.auth.GoogleAccountCredential
import com.google.api.client.json.gson.GsonFactory
import com.google.api.services.gmail.Gmail
import com.google.api.services.gmail.GmailScopes

object GmailServiceHelper {

    fun getService(context: Context): Gmail {

        val credential = GoogleAccountCredential.usingOAuth2(
            context,
            listOf(GmailScopes.GMAIL_SEND)
        )

        val account = GoogleSignIn.getLastSignedInAccount(context)

        credential.selectedAccount = account?.account

        return Gmail.Builder(
            AndroidHttp.newCompatibleTransport(),
            GsonFactory(),
            credential
        )
            .setApplicationName("MyAI")
            .build()
    }
}