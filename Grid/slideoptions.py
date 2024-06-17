# First choice of sliding surface function
            if iL < -1.5:
               
                duty = int(65536 -pwm_out) + 1000
                pwm.duty_u16(duty)
            if iL > 1.5:
                duty = int (65536- pwm_out) - 1000
                pwm.duty_u16(duty)
            
            if min_pwm < pwm_out < max_pwm:  # maybe greater or equal
                v_ref = BUS
                v_err = -vb + 7 #ref voltage
                v_err_int = v_err_int + v_err 
                v_err_int = saturate(v_err_int, 10000, -10000)  # Saturate the integral error
                v_pi_out = (kp * v_err) + (ki * v_err_int) #+ (ks * v_err if vb>BUS+0.5) - ks * (v_err if vb<BUS-0.5)
                if slide > 0.1:
                    v_pi_out = v_pi_out + 0.1*slide
                if slide < -0.1:
                    v_pi_out = v_pi_out - 0.1*slide
                slide = (v_err_int)*(v_err_int) - 2*(v_err_int)*(v_err) + (v_err)*(v_err)
                   
                pwm_out = saturate(v_pi_out,max_pwm,min_pwm) 
                duty = int(65536-pwm_out) # Invert because reasons
                pwm.duty_u16(duty) # Send the output of the PI controller out as PWM
            else:
                v_err_int = 0
                pwm_out = 30000
#Second sliding surface function choice below, only one of them will be running on microcontroller
            if min_pwm < pwm_out < max_pwm:  
                        v_ref = BUS
                        v_err = -vb + v_ref #ref voltage
                        v_err_int = v_err_int + v_err 
                        v_err_int = saturate(v_err_int, 10000, -10000)  # Saturate the integral error
                        v_pi_out = (kp * v_err) + (ki * v_err_int) #+ (ks * v_err if vb>BUS+0.5) - ks * (v_err if vb<BUS-0.5)
                        diff = v_err-previous
                        slide = saturate(50*v_err + 10*diff,40000,-40000)
                        if v_err > 0.1:   # that means reference voltage is greater, so increase duty
                             v_pi_out = saturate(v_pi_out - slide,max_pwm,min_pwm)
                        if v_err < -0.1: # that means reference voltage is smaller than vb , vb must decrease
                             v_pi_out = saturate(v_pi_out + slide,max_pwm,min_pwm)
