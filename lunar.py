# Translation of:
# https://github.com/kristopherjohnson/lunar-c
# which is a translation of Jim Storer's FOCAL lunar lander.
#
# Created Class and changed goto labels to methods.
#
# Requires Python Version > 2.7

from math import *


class LL(object):

    # Global variables
    A = 0 #  - Altitude (miles)
    G = 0 # - Gravity
    I = 0 # - Intermediate altitude (miles)
    J = 0 # - Intermediate velocity (miles/sec)
    K = 0 # - Fuel rate (lbs/sec)
    L = 0 # - Elapsed time (sec)
    M = 0 # - Total weight (lbs)
    N = 0 # - Empty weight (lbs, Note: M - N is remaining fuel weight)
    S = 0 # - Time elapsed in current 10-second turn (sec)
    T = 0 # - Time remaining in current 10-second turn (sec)
    V = 0 # - Downward speed (miles/sec)
    W = 0 # - Temporary working variable
    Z = 0 # - Thrust per pound of fuel burned
    TESTING = False
    kdata = None

    def apply_thrust(self):
        Q = LL.S * LL.K / LL.M;
        Q_2 = pow(Q, 2);
        Q_3 = pow(Q, 3);
        Q_4 = pow(Q, 4);
        Q_5 = pow(Q, 5);
        LL.J = LL.V + LL.G * LL.S + LL.Z * \
               (-Q - Q_2 / 2 - Q_3 / 3 - Q_4 / 4 - Q_5 / 5);
        LL.I = LL.A - LL.G * LL.S * LL.S / 2 - \
               LL.V * LL.S + LL.Z * LL.S * \
               (Q / 2 + Q_2 / 6 + Q_3 / 12 + Q_4 / 20 + Q_5 / 30)

    def start_turn(self):

        tmp3 = 5280*(LL.A  - floor(LL.A) )
        tmp4 = 3600 * LL.V
        tmp5 = LL.M - LL.N
        print("{:^7.0f}{:^16.0f}{:^7.0f}{:^15.2f}{:^12.1f}".format(LL.L,floor(LL.A), tmp3, tmp4, tmp5 ), end='')

    def turn_loop(self):
        #game loop
        while(True):


            if((LL.M - LL.N) < 0.001):
                self.fuel_out()
                self.on_moon()
                return
            if(LL.T < .001):
                self.start_turn()
                if self.TESTING :

                    self.get_k_from_data()
                else:
                    self.promt_for_k()
            
            LL.S = LL.T

            if (LL.N + LL.S * LL.K - LL.M > 0):
                LL.S = (LL.M - LL.N) / LL.K

            self.apply_thrust()

            if (LL.I <= 0):
                self.until_on_moon()
                return

            if ((LL.V > 0) and (LL.J < 0)):

                while(True):

                    LL.W = (1 - LL.M * LL.G / (LL.Z * LL.K)) / 2
                    LL.S = LL.M * LL.V / (LL.Z * LL.K * \
                                          (LL.W + \
                                           sqrt(LL.W * \
                                            LL.W + LL.V / LL.Z))) + 0.5
                    self.apply_thrust();

                    if (LL.I <= 0):
                        self.until_on_moon()
                        return

                    self.update_state();

                    if (-LL.J < 0):
                        #This is recursive all the sundden!!!!
                        self.turn_loop()
                        return
                    if (LL.V <= 0):
                        #This is recursive all the sundden!!!!
                        #print("Downward Velocity is Negative")
                        self.turn_loop()
                        return

                    print("w???")


            self.update_state()



    def update_state(self):

        LL.L += LL.S;
        LL.T -= LL.S;
        LL.M -= LL.S * LL.K;
        LL.A = LL.I;
        LL.V = LL.J;

    def get_k_from_data(self):
        LL.K = self.kdata.pop()
        print("TK:{}".format(LL.K))
        LL.T = 10
        
    def promt_for_k(self):
        done = False
        
        while(not(done)):
            LL.K = float(input("K=:"))
            if(not(LL.K < 0 or ((0 < LL.K) and (LL.K < 8)) or LL.K > 200)):
                done = True
            else:
                print("NOT POSSIBLE")

        LL.T = 10   


    def until_on_moon(self):

        while (LL.S >= .005):
            LL.S = 2 * LL.A / (LL.V + sqrt(LL.V * LL.V + 2 * LL.A * \
                                           (LL.G - LL.Z * LL.K / LL.M)))
            self.apply_thrust()
            self.update_state()
        self.on_moon()


    def on_moon(self):

        print("ON THE MOON AT {:^8.2f} SECS".format(LL.L))
        LL.W = 3600 * LL.V
        print("IMPACT VELOCITY OF {:^8.2f} M.P.H.".format(LL.W))
        print("FUEL LEFT: {:^8.2f} LBS".format( LL.M - LL.N))
        if (LL.W <= 1):
            print("PERFECT LANDING !-(LUCKY)")
        elif (LL.W <= 10):
            print("GOOD LANDING-(COULD BE BETTER)")
        elif (LL.W <= 22):
            print("CONGRATULATIONS ON A POOR LANDING")
        elif (LL.W <= 40):
            print("CRAFT DAMAGE. GOOD LUCK")
        elif (LL.W <= 60):
            print("CRASH LANDING-YOU'VE 5 HRS OXYGEN")
        else:
            print("SORRY,BUT THERE WERE NO SURVIVORS-YOU BLEW IT!")
            print("IN FACT YOU BLASTED A NEW LUNAR CRATER {:^8.2f} FT. DEEP".format( LL.W * .277777))


    def fuel_out(self):
        print("FUEL OUT AT {:^8.2f} SECS".format(LL.L))
        LL.S = (sqrt(LL.V * LL.V + 2 * LL.A * LL.G) - LL.V) / LL.G
        LL.V += LL.G * LL.S
        LL.L += LL.S


    def initMsg(self):
        print("CONTROL CALLING LUNAR MODULE. MANUAL CONTROL IS NECESSARY")
        print("YOU MAY RESET FUEL RATE K EACH 10 SECS TO 0 OR ANY VALUE")
        print("BETWEEN 8 & 200 LBS/SEC. YOU'VE 16000 LBS FUEL. ESTIMATED")
        print("FREE FALL IMPACT TIME-120 SECS. CAPSULE WEIGHT-32500 LBS\n\n")

    def play(self):
        LL.A = 120
        LL.V = 1
        LL.M = 32500
        LL.N = 16500
        LL.G = .001
        LL.Z = 1.8
        LL.L = 0

        print("FIRST RADAR CHECK COMING UP\n\n")
        print("COMMENCE LANDING PROCEDURE")
        print("TIME,SECS   ALTITUDE,MILES+FEET   VELOCITY,MPH  \
 FUEL,LBS   FUEL RATE")
        self.start_turn()
        if self.TESTING :
            
            self.get_k_from_data()
        else:
            self.promt_for_k()
        self.turn_loop()



def test(kdata):
    if kdata == None:
        print("Error - testing requires data!")
    else:
        print("Setup Testing...")
        t = LL()
        kdata.reverse()
        t.kdata = kdata
        print("setting kdata {}".format(t.kdata))
        t.TESTING = True
        print("setting TESTING={}".format(t.TESTING))
        t.play()
        

    
        
def main():
    
    l = LL()
    l.initMsg()
    l.play()
    return l

if __name__ == "__main__":
    main()

