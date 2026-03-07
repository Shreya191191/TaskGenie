package com.aishreya.taskgenie

import android.os.Bundle
import android.util.Log
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.result.contract.ActivityResultContracts
import com.aishreya.taskgenie.tools.gmail.GoogleSignInHelper
import com.aishreya.taskgenie.ui.theme.AIChatScreen
import com.aishreya.taskgenie.ui.theme.TaskGenieTheme
import com.aishreya.taskgenie.viewmodel.AIViewModel
import com.google.android.gms.auth.api.signin.GoogleSignIn
import com.google.android.gms.common.api.ApiException

class MainActivity : ComponentActivity() {

    private val viewModel = AIViewModel()

    private val signInLauncher =
        registerForActivityResult(
            ActivityResultContracts.StartActivityForResult()
        ) { result ->

            val task = GoogleSignIn.getSignedInAccountFromIntent(result.data)

            try {

                val account = task.getResult(ApiException::class.java)

                Log.d("LOGIN_DEBUG", "Login success: ${account.email}")

            } catch (e: ApiException) {

                Log.d("LOGIN_DEBUG", "Login failed code: ${e.statusCode}")
            }
        }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val client = GoogleSignInHelper.getClient(this)

        val account = GoogleSignIn.getLastSignedInAccount(this)

        if (account == null) {
            signInLauncher.launch(client.signInIntent)
        }
        setContent {
            TaskGenieTheme {
                AIChatScreen(viewModel)
                }
            }
        }
    }
