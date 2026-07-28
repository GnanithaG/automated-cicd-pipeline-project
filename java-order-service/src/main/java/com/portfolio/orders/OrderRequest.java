package com.portfolio.orders;

import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotBlank;
import java.math.BigDecimal;

public record OrderRequest(
        @NotBlank String customerId,
        @NotBlank String product,
        @DecimalMin("0.01") BigDecimal amount) {}
