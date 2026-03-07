package com.aishreya.taskgenie.viewmodel


import android.content.Context
import android.util.Log
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.aishreya.taskgenie.agent.AIAgent
import kotlinx.coroutines.launch

class AIViewModel : ViewModel() {

    private val agent = AIAgent()

    fun askAI(context: Context, message: String, onResult: (String) -> Unit) {
        Log.d("VIEWMODEL", "askAI called: $message")
        viewModelScope.launch {

            val result = agent.processMessage(context,message)

            onResult(result)
        }
    }
}