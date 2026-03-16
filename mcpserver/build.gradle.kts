plugins {
    id("application")
    alias(libs.plugins.jetbrains.kotlin.jvm)
    kotlin("plugin.serialization") version "2.0.21"
    id("com.gradleup.shadow") version "8.3.9"
}

val mcpVersion = "0.4.0"
val slf4jVersion = "2.0.9"
val ktorVersion = "3.1.1"

java {
    sourceCompatibility = JavaVersion.VERSION_17
    targetCompatibility = JavaVersion.VERSION_17
}
kotlin {
    compilerOptions {
        jvmTarget = org.jetbrains.kotlin.gradle.dsl.JvmTarget.JVM_17
    }
}
application {
    mainClass.set("com.aishreya.mcpserver.MainKt")
}
dependencies {
    //MCP
    implementation("io.modelcontextprotocol:kotlin-sdk:${mcpVersion}")
    implementation("org.slf4j:slf4j-nop:${slf4jVersion}")
    implementation("io.ktor:ktor-client-content-negotiation:${ktorVersion}")
    implementation("io.ktor:ktor-serialization-kotlinx-json:${ktorVersion}")
}