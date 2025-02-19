package com.fitindia.Fitindiabackend.Services;

import java.util.ArrayList;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.fitindia.Fitindiabackend.Dao.CaloriesDao;
import com.fitindia.Fitindiabackend.Entity.Calories;

@Service
public class FitServiceImpl implements FitServices {

    // List<Calories> calories;
    @Autowired
    private CaloriesDao caloriesDao;

    public FitServiceImpl() {
        // calories = new ArrayList<>();
        // calories.add(new Calories(1L, 100L, 10L, 20L, 30L));
        // calories.add(new Calories(2L, 200L, 20L, 30L, 40L));
    }

    @Override
    public List<Calories> getCalories() {
        return caloriesDao.findAll();
    }

    @Override
    public Calories getCalories(Long id) {
        // return calories.stream().filter(e -> e.getId().equals(id)).findFirst().get();
        return caloriesDao.findById(id).get();
    }

    @Override
    public Calories addCalories(Calories calories) {
        // this.calories.add(calories);
        caloriesDao.save(calories);
        return calories;
    }

    @Override
    public Calories deleteCalories(Long id) {
        // calories.remove(id);
        caloriesDao.deleteById(id);
        return null;
    }

    @Override
    public Long getTotalCalories() {
        Long totalCalories = 0L;

        List<Calories> calories = caloriesDao.findAll();
        for (Calories c : calories) {
            totalCalories += c.getCalories();
        }
        return totalCalories;
    }

}
