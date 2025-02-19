package com.fitindia.Fitindiabackend.Controller;

import java.nio.channels.Pipe.SourceChannel;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.servlet.ModelAndView;

import com.fitindia.Fitindiabackend.Entity.Calories;
import com.fitindia.Fitindiabackend.Services.FitServices;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;

@RestController
// @Controller
public class FitController {

    @Autowired
    private FitServices caloriesService;

    @RequestMapping("/home")
    // @ResponseBody
    public ModelAndView home(Model model) {
        ModelAndView modelAndView = new ModelAndView();
        modelAndView.setViewName("Home.html");
        return modelAndView;
    }

    @RequestMapping("/dashboard")
    // @ResponseBody
    public ModelAndView dashboard(Model model) {
        ModelAndView modelAndView = new ModelAndView();
        modelAndView.setViewName("Dashboard.html");
        return modelAndView;
    }

    @RequestMapping("/signup")
    // @ResponseBody
    public ModelAndView signup(Model model) {
        ModelAndView modelAndView = new ModelAndView();
        modelAndView.setViewName("Signup.html");
        return modelAndView;
    }

    @RequestMapping("/login")
    // @ResponseBody
    public ModelAndView login(Model model) {
        ModelAndView modelAndView = new ModelAndView();
        modelAndView.setViewName("Login.html");
        return modelAndView;
    }

    @RequestMapping("/dietplan")
    // @ResponseBody
    public ModelAndView dietplan(Model model) {
        ModelAndView modelAndView = new ModelAndView();
        modelAndView.setViewName("Dietplan.html");
        return modelAndView;
    }

    @RequestMapping("/caloriecalculator")
    // @ResponseBody
    public ModelAndView caloriecalculator(Model model) {
        ModelAndView modelAndView = new ModelAndView();
        modelAndView.setViewName("Caloriecalculator.html");
        return modelAndView;
    }

    // getting calories
    @GetMapping("/calories")
    public List<Calories> getMethodName() {
        return caloriesService.getCalories();
    }

    // getting calories by id
    @GetMapping("/calories/{id}")
    public Calories getMethodName(@PathVariable String id) {
        return caloriesService.getCalories(Long.parseLong(id));
    }

    @PostMapping("/add")
    public Calories postMethodName(@RequestBody Calories calories) {
        return caloriesService.addCalories(calories);
    }

    @DeleteMapping("/delete/{id}")
    public ResponseEntity<HttpStatus> deleteCalories(@PathVariable String id) {
        try {
            caloriesService.deleteCalories(Long.parseLong(id));
            return new ResponseEntity<>(HttpStatus.OK);
        } catch (Exception e) {
            return new ResponseEntity<>(HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @GetMapping("/totalcalories")
    public Long getTotalCalories() {
        return caloriesService.getTotalCalories();
    }
}
