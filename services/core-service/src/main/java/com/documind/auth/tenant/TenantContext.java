package com.documind.auth.tenant;

/**
 * Holds the current request's tenant id, extracted from the JWT by JwtAuthFilter.
 * Used to scope document queries so one tenant can never see another tenant's data.
 */
public class TenantContext {

    private static final ThreadLocal<String> CURRENT_TENANT = new ThreadLocal<>();

    public static void setTenantId(String tenantId) {
        CURRENT_TENANT.set(tenantId);
    }

    public static String getTenantId() {
        return CURRENT_TENANT.get();
    }

    public static void clear() {
        CURRENT_TENANT.remove();
    }
}
