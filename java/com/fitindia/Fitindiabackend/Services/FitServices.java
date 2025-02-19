package com.fitindia.Fitindiabackend.Services;

import java.util.List;

import com.fitindia.Fitindiabackend.Entity.Calories;

public interface FitServices {
    public List<Calories> getCalories();

    public Calories getCalories(Long id);

    public Calories addCalories(Calories calories);

    public Calories deleteCalories(Long id);

    public Long getTotalCalories();

    
}
