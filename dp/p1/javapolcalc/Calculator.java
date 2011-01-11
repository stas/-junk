/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package javapolcalc;

/**
 * Singleton Class for Calculator
 * @author stas
 */
public class Calculator {
    Divident divident = new Divident();
    Divider divider = new Divider();
    Result result = new Result();

    private Calculator() {
        this.sum();
    }

    public static Calculator getInstance() {
        return CalculatorHolder.INSTANCE;
    }

    private void sum() {
        this.result.polynom = this.divident.polynom.plus(this.divider.polynom);
        this.result.print();
    }

    private static class CalculatorHolder {
        private static final Calculator INSTANCE = new Calculator();
    }
 }
