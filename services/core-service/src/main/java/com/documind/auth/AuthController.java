package com.documind.auth;

import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

@RestController
@RequestMapping("/auth")
public class AuthController {

    private final JwtService jwtService;
    private final PasswordEncoder passwordEncoder;

    // Demo in-memory user store so the auth flow is runnable end-to-end without
    // a full user-management feature. Replace with a real user repository
    // (email/password signup, hashed on write) before this goes anywhere near
    // production. Demo credentials: demo@documind.dev / demo1234
    private static final Map<String, String> DEMO_USERS = Map.of(
            "demo@documind.dev", "$2b$10$yJRAqytDnQft7C5qEOxa9ewWvboREbik9b7HC6mX5eC1rOPUSup3C"
    );

    public AuthController(JwtService jwtService, PasswordEncoder passwordEncoder) {
        this.jwtService = jwtService;
        this.passwordEncoder = passwordEncoder;
    }

    @PostMapping("/login")
    public LoginResponse login(@RequestBody LoginRequest request) {
        String storedHash = DEMO_USERS.get(request.username());
        if (storedHash == null || !passwordEncoder.matches(request.password(), storedHash)) {
            throw new BadCredentialsException("Invalid credentials");
        }
        String token = jwtService.generateToken(request.username(), request.tenantId());
        return new LoginResponse(token, "Bearer");
    }
}
