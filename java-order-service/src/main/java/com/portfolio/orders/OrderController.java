package com.portfolio.orders;

import jakarta.validation.Valid;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import java.util.concurrent.CopyOnWriteArrayList;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/orders")
public class OrderController {
    private final List<OrderResponse> orders = new CopyOnWriteArrayList<>();

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public OrderResponse create(@Valid @RequestBody OrderRequest request) {
        OrderResponse response = new OrderResponse(
                UUID.randomUUID(), request.customerId(), request.product(), request.amount(),
                "ACCEPTED", Instant.now());
        orders.add(response);
        return response;
    }

    @GetMapping
    public List<OrderResponse> list() {
        return new ArrayList<>(orders);
    }

    @GetMapping("/{id}")
    public OrderResponse get(@PathVariable UUID id) {
        return orders.stream().filter(order -> order.orderId().equals(id)).findFirst()
                .orElseThrow(() -> new OrderNotFoundException(id));
    }
}
