package com.documind.auth;

public record LoginRequest(String username, String password, String tenantId) {}
