package com.aishreya.mcpserver

import io.ktor.utils.io.streams.asInput
import io.modelcontextprotocol.kotlin.sdk.CallToolResult
import io.modelcontextprotocol.kotlin.sdk.Implementation
import io.modelcontextprotocol.kotlin.sdk.ServerCapabilities
import io.modelcontextprotocol.kotlin.sdk.TextContent
import io.modelcontextprotocol.kotlin.sdk.server.Server
import io.modelcontextprotocol.kotlin.sdk.server.ServerOptions
import io.modelcontextprotocol.kotlin.sdk.server.StdioServerTransport
import kotlinx.coroutines.Job
import kotlinx.coroutines.runBlocking
import kotlinx.io.asSink
import kotlinx.io.buffered
// Main function to run the MCP server
fun main() {
    val server = Server(
        Implementation(
            name = "my-mcp-server",
            version = "1.0.0"
        ),
        ServerOptions(
            capabilities = ServerCapabilities(
                tools = ServerCapabilities.Tools(listChanged = true)
            )
        )
    )

    // WEATHER TOOL
    server.addTool(
        name = "weather",
        description = "Get weather of a city"
    ) { request ->

        val city = request.arguments["city"]?.toString() ?: "Unknown"

        CallToolResult(
            content = listOf(
                TextContent(
                    text = "Weather in $city is 30°C and sunny"
                )
            )
        )
    }

    // EMAIL TOOL
    server.addTool(
        name = "send_mail",
        description = "Send email"
    ) { request ->

        val to = request.arguments["to"]?.toString() ?: ""
        val message = request.arguments["message"]?.toString() ?: ""

        println("Sending email to $to : $message")

        CallToolResult(
            content = listOf(
                TextContent(
                    text = "Email sent successfully"
                )
            )
        )
    }

    val transport = StdioServerTransport(
        System.`in`.asInput(),
        System.out.asSink().buffered()
    )

    runBlocking {

        server.connect(transport)

        val done = Job()

        server.onClose {
            done.complete()
        }

        done.join()
    }
}