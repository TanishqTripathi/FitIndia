package com.fitindia.Fitindiabackend.Entity;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.OneToOne;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;

@Data
@Entity
@AllArgsConstructor
@Builder
public class Calories {

    @Id
    // @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private Long Calories;
    private Long Protien;
    private Long Carbs;
    private Long Fats;

    public Calories(Long calories, Long protien, Long carbs, Long fats) {
        // this.id = id;
        this.Calories = calories;
        this.Protien = protien;
        this.Carbs = carbs;
        this.Fats = fats;
    }

    public Calories() {
    }

    @OneToOne
    private User user;
}
