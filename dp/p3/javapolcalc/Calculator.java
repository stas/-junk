/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package javapolcalc;

import com.sun.istack.internal.NotNull;
import java.util.Collection;

/**
 * Singleton Class for Calculator
 * @author stas
 */
public class Calculator {
    Divident divident = new Divident();
    Divider divider = new Divider();
    Result result = new Result();
    
    private Memento previousResult = null;

    public Calculator() {
        this.sum();
    }

    public void reinit() {
        this.sum();
    }

    private void sum() {
        this.result.polynom = this.divident.polynom.plus(this.divider.polynom);
        this.result.print();
    }

    public Memento saveToMemento(){
        if ( previousResult == null )
            previousResult = new Memento( this );
        return previousResult;
    }

    public void restoreFromMemento(){
        if( previousResult != null ) {
            System.out.println("Previous operations were:");
            System.out.println(previousResult.divider.polynom.toString());
            System.out.println(previousResult.divident.polynom.toString());
            this.divident = previousResult.divident;
            this.divider = previousResult.divider;
        }
    }

    public static class Memento {
        private final Divident divident;
        private final Divider divider;

        private Memento( Calculator c ) {
            divident = c.divident;
            divider = c.divider;
        }

        private Memento getMemento() {
            return this;
        }
    }
 }
