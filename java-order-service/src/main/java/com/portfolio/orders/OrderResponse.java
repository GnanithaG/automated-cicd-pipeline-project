package com.portfolio.orders;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.UUID;

public record OrderResponse(
        UUID orderId,
        String customerId,
        String product,
        BigDecimal amount,
        String status,
        Instant createdAt) {}
