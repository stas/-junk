/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package javapolcalc;

/**
 * Class for generating a polynomial object with its afferent methods
 * A library for polynomial math calculations
 * @author stas
 */
public class Polynomial {
    private int[] coef;  // coefficients
    private int deg;     // degree of polynomial (0 for the zero polynomial)

    /**
     * Method calculates and returns a * x^b
     * Class constructor
     */
    public Polynomial(int a, int b) {
        coef = new int[b + 1];
        coef[b] = a;
        deg = degree();
    }

    /**
     * Method calculates and returns the degree of this polynomial (0 for the zero polynomial)
     * @return  degree of the polynomial
     */
    public int degree() {
        int d = 0;
        for (int i = 0; i < coef.length; i++) {
            if (coef[i] != 0) {
                d = i;
            }
        }
        return d;
    }

    /**
     * Method calculates and returns c = a + b
     * @param   b - a Plynomial object to sum with
     * @return  a new Polynomial object as a result
     */
    public Polynomial plus(Polynomial b) {
        Polynomial a = this;
        Polynomial c = new Polynomial(0, Math.max(a.deg, b.deg));
        for (int i = 0; i <= a.deg; i++) {
            c.coef[i] += a.coef[i];
        }
        for (int i = 0; i <= b.deg; i++) {
            c.coef[i] += b.coef[i];
        }
        c.deg = c.degree();
        return c;
    }

    /**
     * Method calculates and returns (a - b)
     * @param b a Polynomial object to extract
     * @return a Plynomial object as a result
     */
    public Polynomial minus(Polynomial b) {
        Polynomial a = this;
        Polynomial c = new Polynomial(0, Math.max(a.deg, b.deg));
        for (int i = 0; i <= a.deg; i++) {
            c.coef[i] += a.coef[i];
        }
        for (int i = 0; i <= b.deg; i++) {
            c.coef[i] -= b.coef[i];
        }
        c.deg = c.degree();
        return c;
    }

    /**
     * Method calculates and returns (a * b)
     * @param b a Polynomial object to sum with
     * @return a Polynomial object as a result
     */
    public Polynomial times(Polynomial b) {
        Polynomial a = this;
        Polynomial c = new Polynomial(0, a.deg + b.deg);
        for (int i = 0; i <= a.deg; i++) {
            for (int j = 0; j <= b.deg; j++) {
                c.coef[i + j] += (a.coef[i] * b.coef[j]);
            }
        }
        c.deg = c.degree();
        return c;
    }

    /**
     * Method calculates and returns (a / b)
     * Using the Ruffini's algorithm, yet uncomplete
     * <a href="http://en.wikipedia.org/wiki/Ruffini%27s_rule#Polynomial_division_by_x_.E2.88.92_r">
     * http://en.wikipedia.org/wiki/Ruffini%27s_rule</a>
     */
    public Polynomial division(Polynomial b) {
        Polynomial a = this;
        Polynomial c = new Polynomial(a.deg, b.deg);
        for (int i = 0; i <= a.deg; i++) {
            for (int j = 0; j <= b.deg; j++) {
                // skip divisions by zero and check degrees
                if((a.coef[i] != 0 && b.coef[j] != 0) && i >= j )
                    c.coef[i - j] += (a.coef[i] / b.coef[j]);
                else {
                    if(i >= j)
                        c.coef[i-j] += 0;
                }
            }
        }
        c.deg = c.degree();
        return c;
    }

    /**
     * Method calculates and returns a(b(x))  - compute using Horner's method
     * @param b a Polynomial object to compose with
     * @return  a Polynomial object as a result
     */
    public Polynomial compose(Polynomial b) {
        Polynomial a = this;
        Polynomial c = new Polynomial(0, 0);
        for (int i = a.deg; i >= 0; i--) {
            Polynomial term = new Polynomial(a.coef[i], 0);
            c = term.plus(b.times(c));
        }
        return c;
    }


    /**
     * Method checks does a and b represents the same polynomial?
     * @param b a Polynomial object to compare with
     * @return <code>true</code> if the same, <false> if not the same
     */
    public boolean eq(Polynomial b) {
        Polynomial a = this;
        if (a.deg != b.deg) {
            return false;
        }
        for (int i = a.deg; i >= 0; i--) {
            if (a.coef[i] != b.coef[i]) {
                return false;
            }
        }
        return true;
    }


    /**
     * Method uses Horner's method to compute and return the polynomial evaluated at x
     * @param   x an integer to evaluate at
     * @return  thre results of evalution as an integer
     */
    public int evaluate(int x) {
        int p = 0;
        for (int i = deg; i >= 0; i--) {
            p = coef[i] + (x * p);
        }
        return p;
    }

    /**
     * Method differentiates this polynomial and returns it
     * @return  a Polynomial object which represents the result.
     */
    public Polynomial differentiate() {
        if (deg == 0) {
            return new Polynomial(0, 0);
        }
        Polynomial deriv = new Polynomial(0, deg - 1);
        deriv.deg = deg - 1;
        for (int i = 0; i < deg; i++) {
            deriv.coef[i] = (i + 1) * coef[i + 1];
        }
        return deriv;
    }

    /**
     * Method converts to string representation
     * @return the converted string of the Polynomial object
     */
    public String toString() {
        if (deg == 0) {
            return "" + coef[0];
        }
        if (deg == 1) {
            return coef[1] + "x+" + coef[0];
        }
        String s = coef[deg] + "x^" + deg;
        for (int i = deg - 1; i >= 0; i--) {
            if (coef[i] == 0) {
                continue;
            } else if (coef[i] > 0) {
                s = s + "+" + (coef[i]);
            } else if (coef[i] < 0) {
                s = s + "-" + (-coef[i]);
            }
            if (i == 1) {
                s = s + "x";
            } else if (i > 1) {
                s = s + "x^" + i;
            }
        }
        return s;
    }
}
