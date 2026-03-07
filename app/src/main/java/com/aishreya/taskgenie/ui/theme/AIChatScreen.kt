package com.aishreya.taskgenie.ui.theme

import android.util.Log
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.ui.platform.LocalContext
import com.aishreya.taskgenie.viewmodel.AIViewModel

@Composable
fun AIChatScreen(viewModel: AIViewModel) {

    val context = LocalContext.current

    var input by remember { mutableStateOf("") }
    var response by remember { mutableStateOf("") }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {

        Text(
            text = "AI Agent",
            style = MaterialTheme.typography.headlineMedium
        )

        Spacer(modifier = Modifier.height(20.dp))

        TextField(
            value = input,
            onValueChange = { input = it },
            label = { Text("Ask something") },
            modifier = Modifier.fillMaxWidth()
        )

        Spacer(modifier = Modifier.height(12.dp))
        Button(onClick = {

            Log.d("MY_DEBUG", "Button clicked with input = $input")

            viewModel.askAI(context, input) { result ->
                Log.d("MY_DEBUG", "Result received = $result")
                response = result
            }

        }) {
            Text("Send")
        }

        Spacer(modifier = Modifier.height(20.dp))

        Text(text = "Response:")

        Text(text = response)
    }
}