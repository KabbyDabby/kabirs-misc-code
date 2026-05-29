import java.util.Arrays;

/**
 * Self-contained test using the EXACT Smile library implementation. Source copied directly from:
 * github.com/haifengl/smile/base/src/main/java/smile/interpolation/
 *
 * Key finding: Smile's AbstractInterpolation.locate() checks boolean ascnd = (xx[n-1] >= xx[0]) and
 * handles BOTH ascending and descending arrays.
 */
public class BilinearInterpolationTest {

    // ========================================================================
    // EXACT COPY of smile.interpolation.AbstractInterpolation
    // ========================================================================
    static abstract class AbstractInterpolation {
        private final int dj;
        private int jsav;
        private boolean cor;
        int n;
        double[] xx;
        double[] yy;

        public AbstractInterpolation(double[] x, double[] y) {
            if (x.length != y.length) {
                throw new IllegalArgumentException("x and y have different length");
            }

            this.n = x.length;

            if (n < 2) {
                throw new IllegalArgumentException("locate size error");
            }

            this.xx = x;
            this.yy = y;

            jsav = 0;
            cor = false;
            dj = Math.min(1, (int) Math.pow(n, 0.25));
        }

        public double interpolate(double x) {
            int jlo = search(x);
            return rawinterp(jlo, x);
        }

        protected int search(double x) {
            return cor ? hunt(x) : locate(x);
        }

        private int locate(double x) {
            int ju, jm, jl;

            boolean ascnd = (xx[n - 1] >= xx[0]);

            jl = 0;
            ju = n - 1;
            while (ju - jl > 1) {
                jm = (ju + jl) >> 1;
                if (x >= xx[jm] == ascnd) {
                    jl = jm;
                } else {
                    ju = jm;
                }
            }

            cor = Math.abs(jl - jsav) <= dj;
            jsav = jl;

            return Math.max(0, Math.min(n - 2, jl));
        }

        private int hunt(double x) {
            int jl = jsav, jm, ju, inc = 1;

            boolean ascnd = (xx[n - 1] >= xx[0]);

            if (jl < 0 || jl > n - 1) {
                jl = 0;
                ju = n - 1;
            } else {
                if (x >= xx[jl] == ascnd) {
                    for (;;) {
                        ju = jl + inc;
                        if (ju >= n - 1) {
                            ju = n - 1;
                            break;
                        } else if (x < xx[ju] == ascnd) {
                            break;
                        } else {
                            jl = ju;
                            inc += inc;
                        }
                    }
                } else {
                    ju = jl;
                    for (;;) {
                        jl = jl - inc;
                        if (jl <= 0) {
                            jl = 0;
                            break;
                        } else if (x >= xx[jl] == ascnd) {
                            break;
                        } else {
                            ju = jl;
                            inc += inc;
                        }
                    }
                }
            }

            while (ju - jl > 1) {
                jm = (ju + jl) >> 1;
                if (x >= xx[jm] == ascnd) {
                    jl = jm;
                } else {
                    ju = jm;
                }
            }

            cor = Math.abs(jl - jsav) <= dj;
            jsav = jl;
            return Math.max(0, Math.min(n - 2, jl));
        }

        public abstract double rawinterp(int jlo, double x);
    }

    // ========================================================================
    // EXACT COPY of smile.interpolation.LinearInterpolation
    // ========================================================================
    static class LinearInterpolation extends AbstractInterpolation {
        public LinearInterpolation(double[] x, double[] y) {
            super(x, y);
        }

        @Override
        public double rawinterp(int j, double x) {
            if (xx[j] == xx[j + 1]) {
                return yy[j];
            } else {
                return yy[j] + ((x - xx[j]) / (xx[j + 1] - xx[j])) * (yy[j + 1] - yy[j]);
            }
        }
    }

    // ========================================================================
    // EXACT COPY of smile.interpolation.BilinearInterpolation
    // ========================================================================
    static class BilinearInterpolation {
        private final double[][] y;
        private final LinearInterpolation x1terp;
        private final LinearInterpolation x2terp;

        public BilinearInterpolation(double[] x1, double[] x2, double[][] y) {
            if (x1.length != y.length) {
                throw new IllegalArgumentException("x1.length != y.length");
            }

            if (x2.length != y[0].length) {
                throw new IllegalArgumentException("x2.length != y[0].length");
            }

            this.y = y;
            x1terp = new LinearInterpolation(x1, x1);
            x2terp = new LinearInterpolation(x2, x2);
        }

        public double interpolate(double x1, double x2) {
            int i = x1terp.search(x1);
            int j = x2terp.search(x2);

            double t = (x1 - x1terp.xx[i]) / (x1terp.xx[i + 1] - x1terp.xx[i]);
            double u = (x2 - x2terp.xx[j]) / (x2terp.xx[j + 1] - x2terp.xx[j]);

            return (1. - t) * (1. - u) * y[i][j] + t * (1. - u) * y[i + 1][j]
                    + (1. - t) * u * y[i][j + 1] + t * u * y[i + 1][j + 1];
        }
    }

    // ========================================================================
    // Test
    // ========================================================================

    static final double GOAL_X = 6.0;
    static final double GOAL_Y = 135.5;
    static final double SHOOTER_OFFSET_X = -1.346;

    static double getXDistance(double xPos) {
        return Math.abs(GOAL_X - (xPos + 1.062));
    }

    static double getYDistance(double yPos) {
        return Math.abs(GOAL_Y - (yPos + SHOOTER_OFFSET_X - 1.436));
    }

    public static void main(String[] args) {
        double[] xPositions = {22.75, 46.75, 58.75, 70.75, 82.75, 94.75, 118.75};
        double[] xDistances = new double[xPositions.length];
        for (int i = 0; i < xPositions.length; i++)
            xDistances[i] = getXDistance(xPositions[i]);

        // ============ DESCENDING yDistances ============
        double[] yPosBefore = {11.375, 22.75, 46.75, 70.75, 94.75, 118.75};
        double[] yDistBefore = new double[yPosBefore.length];
        for (int i = 0; i < yPosBefore.length; i++)
            yDistBefore[i] = getYDistance(yPosBefore[i]);

        double[][] flywheelBefore = {{1839, 1753, 1612, 1497, 1434, 1434},
                {1903, 1862, 1676, 1541, 1420, 1370}, {1973, 1892, 1799, 1558, 1410, 1443},
                {2120, 1960, 1815, 1579, 1496, 1475}, {2215, 2039, 1848, 1631, 1544, 1473},
                {2201, 2016, 1889, 1734, 1612, 1584}, {2320, 2266, 2075, 1912, 1810, 1772},};

        // ============ ASCENDING yDistances ============
        double[] yPosAfter = {118.75, 94.75, 70.75, 46.75, 22.75, 11.375};
        double[] yDistAfter = new double[yPosAfter.length];
        for (int i = 0; i < yPosAfter.length; i++)
            yDistAfter[i] = getYDistance(yPosAfter[i]);

        double[][] flywheelAfter = {{1434, 1434, 1497, 1612, 1753, 1839},
                {1370, 1420, 1541, 1676, 1862, 1903}, {1443, 1410, 1558, 1799, 1892, 1973},
                {1475, 1496, 1579, 1815, 1960, 2120}, {1473, 1544, 1631, 1848, 2039, 2215},
                {1584, 1612, 1734, 1889, 2016, 2201}, {1772, 1810, 1912, 2075, 2266, 2320},};

        // Print axes
        System.out.println("=== X Distances ===");
        for (double d : xDistances)
            System.out.printf("  %.2f", d);
        System.out.println();

        System.out.println("\nDESCENDING yDistances:");
        for (double d : yDistBefore)
            System.out.printf("  %.2f", d);
        System.out.println();

        System.out.println("\nASCENDING yDistances:");
        for (double d : yDistAfter)
            System.out.printf("  %.2f", d);
        System.out.println();

        // Build interpolators
        BilinearInterpolation interpBefore =
                new BilinearInterpolation(xDistances, yDistBefore, flywheelBefore);
        BilinearInterpolation interpAfter =
                new BilinearInterpolation(xDistances, yDistAfter, flywheelAfter);

        // Test at multiple robot positions
        double[][] testPoses = {{70.75, 22.75}, {46.75, 46.75}, {58.75, 70.75}, {70.75, 70.75},
                {82.75, 94.75}, {94.75, 118.75},};

        System.out.println("\n=== Results (using EXACT Smile implementation) ===");
        System.out.printf("  %-16s %7s %7s | %10s %10s %8s%n", "Robot Pos", "dx", "dy", "DESC",
                "ASC", "Delta");
        System.out.println("  " + "-".repeat(68));

        for (double[] pose : testPoses) {
            double shooterX = pose[0] + SHOOTER_OFFSET_X;
            double dx = Math.abs(GOAL_X - shooterX);
            double dy = Math.abs(GOAL_Y - pose[1]);

            double before = interpBefore.interpolate(dx, dy);
            double after = interpAfter.interpolate(dx, dy);

            System.out.printf("  (%.1f, %.1f)  %7.2f %7.2f | %10.1f %10.1f %8.1f%n", pose[0],
                    pose[1], dx, dy, before, after, Math.abs(before - after));
        }

        // Detailed breakdown
        double mainDx = Math.abs(GOAL_X - (70.75 + SHOOTER_OFFSET_X));
        double mainDy = Math.abs(GOAL_Y - 70.75);
        System.out.printf("%n=== Detailed: robot at (70.75, 70.75), dx=%.3f dy=%.3f ===%n", mainDx,
                mainDy);
        System.out.printf("  DESCENDING: %.2f TPS%n", interpBefore.interpolate(mainDx, mainDy));
        System.out.printf("  ASCENDING:  %.2f TPS%n", interpAfter.interpolate(mainDx, mainDy));
    }
}
