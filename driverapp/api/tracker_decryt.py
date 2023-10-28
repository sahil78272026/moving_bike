def motion_value(value):
    if value=="11":
        data="stop"
    elif value=="10":
        data="start"
    elif value=="01":
        data="in motion"
    elif value=="00":
        data="Immobile "
    else:
        data=None
    return data

def tilt_sixd_position(value):
    if value =="000":
        data="Disabled"
    elif value =="001":
        data="Y High"
    elif value =="010":
        data="Y Low"
    elif value =="011":
        data="X High"
    elif value =="100":
        data="X Low"
    elif value =="101":
        data="Z High"
    elif value =="110":
        data="Z Low"
    else:
        pass
    return data

def binaryToDecimal(n):
    return int(n,2)

# n='0100000'
# print(binaryToDecimal(n))

def HexaToDecimal(n):
    return int(n,16)

def HexaToDecimaconvetGPS(n):
    hexa_data= int(n,16)
    if len(str(hexa_data))==1:
        data='0'+str(hexa_data)
    else:
        data=hexa_data

    return data

def hex_to_binary(hex_number: str, num_digits: int = 8) -> str:
    return str(bin(int(hex_number, 16)))[2:].zfill(num_digits)

def realtime_check(n1,n2):
    if n1 !="00" and n2 !="00":
        data=HexaToDecimal(n1+n2)
    elif n1=="00" and n2 =="00":
        data="RealTime"
    elif n2 !="00":
        data=HexaToDecimal(n2)
    elif n1 !="00":
        data=HexaToDecimal(n1)
    else:
        pass
    return data

def voltage(value):
    if value>100:
        value = ((value-2800)*100)/(4300-2800);
    return value

def binaryToHexa(n):
    return f'{int(n, 2):X}'
# print(binaryToHexa('010000'))

def downlink_type_o4_bit(value):
    if value=='0000':
        data="Any"
    elif value=='0001':
        data="RTC"
    elif value=="0010":
        data="Data Configuration"
    elif value=="0011":
        data="Module Configuration"
    elif value=="0101":
        data="Asset Locator Configuration",
    elif value=="0110":
        data="Wi-Fi Configuration"
    elif value=="0111":
        data="Wi-Fi Credentials"
    elif value=='1111':
        data="Default"
    else:
        data=None
    return data


def device_information_ten(value):
    # print(value)
    if value[-1]=="1":
        data="Working"
    elif value[-4]=="1":
        data="Working"
    elif value[-6]=="1":
        data="Working"
    elif value[-1]=="0":
        data="Not Working"
    elif value[-4]=="0":
        data="Not Working"
    elif value[-6]=="0":
        data="Not Working"
    else:
        pass
    return data

def device_information_fuel(value):
    if value[-8]=="1":
        data="NON Rechargeable"
    elif value[-7]=="1":
        data="Rechargeable"
    else:
        data=None
    
    return data
def device_temperature_humidity(value):
    if value[-3]=="1":
        data="Working "
    else:
        data="Non Working "
    return data

def device_information_EPROM(value):
    if value[-1]=="1":
        data="Working"
    elif value[-2]=="1":
        data="Working"
    elif value[-3]=="1":
        data="Working"
    elif value[-1]=="0":
        data="Not Working"
    elif value[-2]=="0":
        data="Not Working"
    elif value[-3]=="0":
        data="Not Working"
    else:
        pass
    return data

def alert_type(value):
    if value=='0000':
        data="Tilt"
    elif value=='0001':
        data="STOP - START"
    elif value=="0010":
        data="START - STOP"
    elif value=="0011":
        data="Fall Detection"
    elif value=="0100":
        data="Low Battery",
    elif value=="0101":
        data="Temperature"
    elif value=="0110":
        data="Humidity"
    elif value=='0111':
        data="Theft"
    else:
        data=None
    return data 


#--------------------09 alert data description data start---------------



alert_dict={
    '0000':"Tilt",
    '0001':"STOP - START",
    "0010":"START - STOP",
    "0011":"Fall Detection",
    "0100":"Low Battery",
    "0101":"Temperature",
    "0110":"Humidity",
    '0111':"Theft"
}
def alert_tilt(value):
    if value=='0000':
        data=alert_dict['0000']
    else:
        data=None
    return data
    
def alert_motion_start(value):
    if value=='0001':
        data=alert_dict['0001']
    elif value=='0010':
        data=alert_dict['0010']
    else:
        data=None
    return data
def alert_fall_detetion(value):
    if value=='0011':
        data=alert_dict['0011']
    else:
        data=None
    return data

def alert_low_battery(value):
    if value=='0100':
        data=alert_dict['0100']
    else:
        data=None
    return data

def alert_temperature(value):
    if value=='0101':
        data=alert_dict['0101']
    else:
        data=None
    return data
def alert_humidity(value):
    if value=='0110':
        data=alert_dict['0110']
    else:
        data=None
    return data

def alert_theft(value):
    if value=='0111':
        data=alert_dict['0111'],
    else:
        data=None
    return data

def alert_descryption_data(value,data):
    if value=='Tilt' and len(data)==20:
        print('Tilt data',data)
        bits_1_to_3=data[-3:]  #old Positio
        bits_4=data[-4]
        bits_5_to_7=data[-7:-4:1]
        bits_8_to_20=data[-20:-8:1]
        data={
            'old_position':tilt_sixd_position(bits_1_to_3),
            'bits_4':bits_4,
            'new_position':tilt_sixd_position(bits_5_to_7),
            'bits_8_to_20':bits_8_to_20
        }
    elif (value=="STOP - START" or value=="START - STOP") and len(data)==20:
        bits_1_to_20=data  #RFU

        # data={
        #     'bits_1_to_20':bits_1_to_20
        # }
        data={
            'motion_state':'RFU'
        }
    elif value=="Fall Detection" and len(data)==20:
        bits_1_to_3=data[-3:]  #old Positio
        bits_4=data[-4]
        bits_5_to_7=data[-7:-4:1]
        bits_8_to_20=data[-20:-8:1]

        # data={
        #     'bits_1_to_3':bits_1_to_3,
        #     'bits_4':bits_4,
        #     'bits_5_to_7':bits_5_to_7,
        #     'bits_8_to_20':bits_8_to_20
        # }
        data={
            'old_position':tilt_sixd_position(bits_1_to_3),
            'bits_4':bits_4,
            'new_position':tilt_sixd_position(bits_5_to_7),
            'bits_8_to_20':bits_8_to_20
        }
    elif value=="Low Battery" and len(data)==20:
        # print('data',data)
        bit_1_to_4=data[-4:]
        bit_5_to_20=data[:-4]

        # data={
        #     'bit_1_to_4':bit_1_to_4,
        #     'bit_5_to_20':bit_5_to_20
        # }
       
        battery_data=round(voltage(binaryToDecimal(bit_5_to_20)))
        data={
            'battery_level':battery_data
        }
        
        
    elif value=='Temperature' and len(data)==20:
        
        bits_1=data[-1]  #old Positio
        bits_2_to_4=data[-4:-1:1]
        bits_5_to_12=data[-12:-4:1]
        bits_12_to_20=data[-20:-12:1]
        temprature_ten_sign=["+" if bits_1=='1' else "-"]
        temprature_data_value=binaryToDecimal(bits_5_to_12)
        # data={
        #     'bits_1':bits_1,
        #     'bits_2_to_4':bits_2_to_4,
        #     'bits_5_to_12':bits_5_to_12,
        #     'bits_12_to_20':bits_12_to_20
            
        # }
        data={
            "temperature_sign":temprature_ten_sign[0],
            "temperature":temprature_data_value,
        }
    elif value=='Humidity' and len(data)==20:
        bit_1_to_4=data[-4:]
        bit_5_to_12=data[-12:-4:1]
        bit_13_to_20=data[-20:-12:1]
        # data={
        #     'bit_1_to_4':bit_1_to_4,
        #     'bit_5_to_12':bit_5_to_12,
        #     'bit_13_to_20':bit_13_to_20
        # }
        data={
            'humidity':binaryToDecimal(bit_5_to_12)
        }
    elif value=='Theft' and len(data)==20:
        bit_1_to_20=data[::]
#         data={
#             "bit_1_to_20":bit_1_to_20
#         }   
        data={
            'theft':"RFU"
        }
    else:
        data=None
    return data

#--------------------09 alert data description data End---------------


def tracker_dcryted_payload_01(value,n=2):
    if value[:2]=='01':
        data=[value[i:i+n] for i in range(0, len(value), n)]
        n1=data[0]
        n2=data[1]
        n3=data[2]
        n4=data[3]
        n5=data[4]
        n6=data[5]
        n7=data[6]
        n8=data[7]
        n9=data[8]
        n10=data[9]
        n11=data[10]
        first_value=hex_to_binary(n1)
        downlink_type=downlink_type_o4_bit(first_value[:4])
        firmware_version=n2+n3
        hardware_version=n4+n5+n6+n7
        serial_no=n8+n9
        value_dcrypt_ten=hex_to_binary(n10)
        device_information_value=device_information_ten(value_dcrypt_ten)
        value_dcrypt_11=hex_to_binary(n11)
        rfu_value=binaryToDecimal(value_dcrypt_11[:4])
        pay_load={
            "type":"Device Information",
            "downlink_type":downlink_type,
            "firmware_version":firmware_version,
            "hardware_version":(hardware_version),
            "serial_no":serial_no,
            "accelerometer":device_information_ten(value_dcrypt_ten[-1]),
            "temperature_humidity":device_temperature_humidity(value_dcrypt_ten),
            "temperature":device_information_ten(value_dcrypt_ten),
            "gps":device_information_ten(value_dcrypt_ten),
            "fuel_gauge":device_information_fuel(value_dcrypt_ten),
            "eeprom":device_information_EPROM(value_dcrypt_ten),
            "pressure":device_information_EPROM(value_dcrypt_ten),
            "ambient_light":device_information_EPROM(value_dcrypt_ten),
            "rfu":rfu_value
            
        }
        return pay_load
    
def tracker_dcryted_payload_02(value,n=2):
    if value[:2]=='02' or value[:2]=='22' or value[:2]=='20':
        data=[value[i:i+n] for i in range(0, len(value), n)]
        n1=data[0]
        n2=data[1]
        n3=data[2]
        #==================
        batter_voltage=n2+n3
        voltage_data_value=round(voltage(HexaToDecimal(batter_voltage)))
        first_value=hex_to_binary(n1)
        downlink_type=downlink_type_o4_bit(first_value[:4])
        pay_load={
            "type":"Configuration Request",
            "battery_level":voltage_data_value,
            "downlink_type":downlink_type
            
        }
        return pay_load
    
def tracker_dcryted_payload_03(value,n=2):
    if value[:2]=='03':
        data=[value[i:i+n] for i in range(0, len(value), n)]
        n1=data[0]
        n2=data[1]
        n3=data[2]
        n4=data[3]
        #=============================
        first_value=hex_to_binary(n1)
        downlink_type=downlink_type_o4_bit(first_value[:4])
        batter_voltage=n2+n3
        voltage_data_value=round(voltage(HexaToDecimal(batter_voltage)))
        #======================temperature 
        tempratue_data_bin=hex_to_binary(n4)[:-1]
        temprature_data_value=binaryToDecimal(tempratue_data_bin)
        pay_load={
            "type":"extra uplink",
            "downlink_type":downlink_type,
            "battery_level":voltage_data_value,
            "temperature":temprature_data_value,
        
        }
        return pay_load
  
def tracker_dcryted_payload_04(value,n=2):
    if value[:2]=='04':
        data=[value[i:i+n] for i in range(0, len(value), n)]
        n1=data[0]
        n2=data[1]
        n3=data[2]
        n4=data[3]
        n5=data[4]
        n6=data[5]
        n7=data[6]
        n8=data[7]
        n9=data[8]
        n10=data[9]
        n11=data[10]
        #===============
        first_value=hex_to_binary(n1)
        downlink_type=downlink_type_o4_bit(first_value[:4])
        #=============motion state===========
        motion_state=hex_to_binary(n2)
        motion_data=motion_value(motion_state[-2:])
        #================battery voltage=====================
        secound_data_value=motion_state[:-2]
        voltage_data_value=round(voltage(HexaToDecimal(binaryToHexa(secound_data_value)+n11)))
        #=============mac time=============
        mac_time=realtime_check(n5,n6)
        mac_time_value=mac_time
        #==========================
        """Roll Angel find"""
        hexa_convert_roll=HexaToDecimal(n7)
        roll_value=round((hexa_convert_roll/256)*180,3)
        #=====================================
        """Pitch Angel find"""
        hexa_convert_bin_pitch= hex_to_binary(n8)
        hexa_convert_bin_value=hexa_convert_bin_pitch[1:]
        hexa_convert_bin_values=round((binaryToDecimal(hexa_convert_bin_value)/128)*360,3)
        #==================hex_to_binary_tild=============================
        first_hexa_convert_bin_pitch=hexa_convert_bin_pitch[:1]
        hex_to_binary_nine_digit=hex_to_binary(n9)
        hex_to_binary_tild=first_hexa_convert_bin_pitch+hex_to_binary_nine_digit[-2:]
        #====================humidity_value========
        tilt_sixd_position_value=tilt_sixd_position(hex_to_binary_tild)
        humidity_value=(binaryToDecimal(hex_to_binary_nine_digit[:-2]))*2
        #======================temperature sign=====================
        temprature_ten=hex_to_binary(n10)
        temprature_ten_sign=["+" if temprature_ten[-1]==1 else "-"]

        #======================temperature value=====================
        temprature_ten_data=temprature_ten[:-1]
        temprature_data_value=binaryToDecimal(temprature_ten_data)

        #=============================
        pay_load={
        "type":"sensor data",
        "downlink_type":downlink_type,
        "battery_level":voltage_data_value,
        "temperature":temprature_data_value,
        "humidity":humidity_value,
        "motion_sensor":motion_data,
        "position":tilt_sixd_position_value,
        "roll_angle":roll_value,
        "pitch_angle":hexa_convert_bin_values,
        "mac_time":mac_time_value,
        "temperature_sign":temprature_ten_sign[0],
        
       
        }
        return pay_load
def tracker_dcryted_payload_04_duplicate(value,n=2):
    if value:
        data=[value[i:i+n] for i in range(0, len(value), n)]
        n1=data[0]
        n2=data[1]
        n3=data[2]
        n4=data[3]
        n5=data[4]
        n6=data[5]
        n7=data[6]
        n8=data[7]
        n9=data[8]
        n10=data[9]
        n11=data[10]
        #===============
        first_value=hex_to_binary(n1)
        downlink_type=downlink_type_o4_bit(first_value[:4])
        #=============motion state===========
        motion_state=hex_to_binary(n2)
        motion_data=motion_value(motion_state[-2:])
        #================battery voltage=====================
        secound_data_value=motion_state[:-2]
        voltage_data_value=round(voltage(HexaToDecimal(binaryToHexa(secound_data_value)+n11)))
        #=============mac time=============
        mac_time=realtime_check(n5,n6)
        mac_time_value=mac_time
        #==========================
        """Roll Angel find"""
        hexa_convert_roll=HexaToDecimal(n7)
        roll_value=round((hexa_convert_roll/256)*180,3)
        #=====================================
        """Pitch Angel find"""
        hexa_convert_bin_pitch= hex_to_binary(n8)
        hexa_convert_bin_value=hexa_convert_bin_pitch[1:]
        hexa_convert_bin_values=round((binaryToDecimal(hexa_convert_bin_value)/128)*360,3)
        #==================hex_to_binary_tild=============================
        first_hexa_convert_bin_pitch=hexa_convert_bin_pitch[:1]
        hex_to_binary_nine_digit=hex_to_binary(n9)
        hex_to_binary_tild=first_hexa_convert_bin_pitch+hex_to_binary_nine_digit[-2:]
        #====================humidity_value========
        tilt_sixd_position_value=tilt_sixd_position(hex_to_binary_tild)
        humidity_value=(binaryToDecimal(hex_to_binary_nine_digit[:-2]))*2
        #======================temperature sign=====================
        temprature_ten=hex_to_binary(n10)
        temprature_ten_sign=["+" if temprature_ten[-1]==1 else "-"]

        #======================temperature value=====================
        temprature_ten_data=temprature_ten[:-1]
        temprature_data_value=binaryToDecimal(temprature_ten_data)

        #=============================
        pay_load={
        "type":"sensor data",
        "downlink_type":downlink_type,
        "battery_level":voltage_data_value,
        "temperature":temprature_data_value,
        "humidity":humidity_value,
        "motion_sensor":motion_data,
        "position":tilt_sixd_position_value,
        "roll_angle":roll_value,
        "pitch_angle":hexa_convert_bin_values,
        "mac_time":mac_time_value,
        "temperature_sign":temprature_ten_sign[0],
        
       
        }
        return pay_load
    else:       
        data=[value[i:i+n] for i in range(0, len(value), n)]
        n1=data[0]
        n2=data[1]
        n3=data[2]
        n4=data[3]
        n5=data[4]
        n6=data[5]
        n7=data[6]
        n8=data[7]
        n9=data[8]
        n10=data[9]
        n11=data[10]
        #===============
        first_value=hex_to_binary(n1)
        downlink_type=downlink_type_o4_bit(first_value[:4])
        #=============motion state===========
        motion_state=hex_to_binary(n2)
        motion_data=motion_value(motion_state[-2:])
        #================battery voltage=====================
        secound_data_value=motion_state[:-2]
        voltage_data_value=round(voltage(HexaToDecimal(binaryToHexa(secound_data_value)+n11)))
        #=============mac time=============
        mac_time=realtime_check(n5,n6)
        mac_time_value=mac_time
        #==========================
        """Roll Angel find"""
        hexa_convert_roll=HexaToDecimal(n7)
        roll_value=round((hexa_convert_roll/256)*180,3)
        #=====================================
        """Pitch Angel find"""
        hexa_convert_bin_pitch= hex_to_binary(n8)
        hexa_convert_bin_value=hexa_convert_bin_pitch[1:]
        hexa_convert_bin_values=round((binaryToDecimal(hexa_convert_bin_value)/128)*360,3)
        #==================hex_to_binary_tild=============================
        first_hexa_convert_bin_pitch=hexa_convert_bin_pitch[:1]
        hex_to_binary_nine_digit=hex_to_binary(n9)
        hex_to_binary_tild=first_hexa_convert_bin_pitch+hex_to_binary_nine_digit[-2:]
        #====================humidity_value========
        tilt_sixd_position_value=tilt_sixd_position(hex_to_binary_tild)
        humidity_value=(binaryToDecimal(hex_to_binary_nine_digit[:-2]))*2
        #======================temperature sign=====================
        temprature_ten=hex_to_binary(n10)
        temprature_ten_sign=["+" if temprature_ten[-1]==1 else "-"]

        #======================temperature value=====================
        temprature_ten_data=temprature_ten[:-1]
        temprature_data_value=binaryToDecimal(temprature_ten_data)

        #=============================
        pay_load={
        "type":"sensor data",
        "downlink_type":downlink_type,
        "battery_level":voltage_data_value,
        "temperature":temprature_data_value,
        "humidity":humidity_value,
        "motion_sensor":motion_data,
        "position":tilt_sixd_position_value,
        "roll_angle":roll_value,
        "pitch_angle":hexa_convert_bin_values,
        "mac_time":mac_time_value,
        "temperature_sign":temprature_ten_sign[0],
        
       
    }
    return pay_load

import googlemaps
gmaps = googlemaps.Client(key='AIzaSyDJraB9ewkAmyzoN_Q4lkh4Tw3m_hShXOU')

def tracker_dcryted_payload_07(value,n=2):
    if value[:2]=='07':
        data=[value[i:i+n] for i in range(0, len(value), n)]
        # print('data',data)
        n1=data[0]
        n2=data[1]
        n3=data[2]
        n4=data[3]
        n5=data[4]
        n6=data[5]
        n7=data[6]
        n8=data[7]
        n9=data[8]
        n10=data[9]
        n11=data[10]
        first_value=hex_to_binary(n1)
        downlink_type=downlink_type_o4_bit(first_value[:4])
        #==============latitude value
        lat_degree=HexaToDecimaconvetGPS(n2)
        lat_min1=HexaToDecimaconvetGPS(n3)
        lat_min2=HexaToDecimaconvetGPS(n4)
        lat_min3=HexaToDecimaconvetGPS(n5)
        latitude=str(lat_degree)+"."+str(lat_min1)+str(lat_min2)+str(lat_min3)
        #=============longitude values
        lon_degree=HexaToDecimaconvetGPS(n6)
        lon_min1=HexaToDecimaconvetGPS(n7)
        lon_min2=HexaToDecimaconvetGPS(n8)
        lon_min3=HexaToDecimaconvetGPS(n9)
        mac_time=realtime_check(n10,n11)
        mac_time_value=mac_time
        
        longitude=str(lon_degree)+"."+str(lon_min1)+str(lon_min2)+str(lon_min3)
        geocode_result = gmaps.reverse_geocode((latitude, longitude))
        address = geocode_result[0]['formatted_address']
    
        pay_load={
            "type":"GPS Data",
            "downlink_type":downlink_type,
            "lat_degree":lat_degree,
            "lat_min1":lat_min1,
            "lat_min2":lat_min2,
            'lat_min3':lat_min3,
            "lon_degree":lon_degree,
            "lon_min2":lon_min2,
            "latitude":latitude,
            "longitude":longitude,
            "mac_time":mac_time_value,
            "address":address
            
            
        }
        return pay_load

def tracker_dcryted_payload_09(value,n=2):
    if value[:2]=='09' or value[:1]=='9' or value[:2]=='90' or  value[:2]=='91':
        data=[value[i:i+n] for i in range(0, len(value), n)]
        # print('data',data)
        n1=data[0]
        n2=data[1]
        n3=data[2]
        n4=data[3]
        n5=data[4]
        n6=data[5]
        first_value=hex_to_binary(n1)
        downlink_type=downlink_type_o4_bit(first_value[:4])
        alert_type_two=hex_to_binary(n2)
#         print('alert_type_two',alert_type_two,alert_type_two[4:],alert_type_two[:4])
        alert_type_value=alert_type(alert_type_two[4:])
        value=alert_type_two[4:]
        first_four_binary=alert_type_two[:4]
        third_value_banary=hex_to_binary(n3)
        four_value_banary=hex_to_binary(n4)
#         print('first_four_binary',first_four_binary,'third_value_banary',third_value_banary,'four_value_banary',four_value_banary)
        total_twentity_digit=str(four_value_banary)+str(third_value_banary)+str(first_four_binary)
#         print(total_twentity_digit)
        mac_time=realtime_check(n5,n6)
        mac_time_value=mac_time
        low_battery_level=alert_low_battery(value)
        
        alert_dict_data=alert_dict[alert_type_two[4:]]
#         print('alert_dict_data',alert_dict_data)
        if alert_dict_data=="Tilt":
            result_data=alert_descryption_data(alert_dict_data,total_twentity_digit)
#             print('result_data',result_data)
           
            pay_load={
                "type":"Alert Data",
                "downlink_type":downlink_type,   
                "alerttype":alert_type_value, 
                "battery_level":low_battery_level,
                "low_battery_level":low_battery_level,
                "alert_temperature":alert_temperature(value),
                "alert_humidity":alert_humidity(value),
                "motion_sensor":alert_motion_start(value),
                "tilt":alert_tilt(value),
                "fall_detection":alert_fall_detetion(value),
                "theft":alert_theft(value),
                "mac_time":mac_time_value,
                'old_position':result_data['old_position'],
                'new_position':result_data['new_position'],
                "temperature_sign":None,
                "temperature":None,

            }
            return pay_load
        elif alert_dict_data=="Fall Detection":
            result_data=alert_descryption_data(alert_dict_data,total_twentity_digit)
            pay_load={
                "type":"Alert Data",
                "downlink_type":downlink_type,   
                "alerttype":alert_type_value, 
                "battery_level":low_battery_level,
                "low_battery_level":low_battery_level,
                "alert_temperature":alert_temperature(value),
                "alert_humidity":alert_humidity(value),
                "motion_sensor":alert_motion_start(value),
                "tilt":alert_tilt(value),
                "fall_detection":alert_fall_detetion(value),
                "theft":alert_theft(value),
                "mac_time":mac_time_value,
                'old_position':result_data['old_position'],
                'new_position':result_data['new_position'],
                "temperature_sign":None,
                "temperature":None,

            }
            return pay_load
        elif alert_dict_data=="Low Battery":
            hexa_value=n3+n4
            voltage_data_value=round(voltage(HexaToDecimal(hexa_value)))
            pay_load={
                "type":"Alert Data",
                "downlink_type":downlink_type,   
                "alerttype":alert_type_value, 
                "battery_level":voltage_data_value,
                "low_battery_level":voltage_data_value,
                "alert_temperature":alert_temperature(value),
                "alert_humidity":alert_humidity(value),
                "motion_sensor":alert_motion_start(value),
                "tilt":alert_tilt(value),
                "fall_detection":alert_fall_detetion(value),
                "theft":alert_theft(value),
                "mac_time":mac_time_value,
                'old_position':None,
                'new_position':None,
                "temperature_sign":None,
                "temperature":None,

            }
            return pay_load
        elif alert_dict_data=="Temperature":
            result_data=alert_descryption_data(alert_dict_data,total_twentity_digit)
            temperature_sign=result_data['temperature_sign']
            temperature=result_data['temperature']
            pay_load={
                "type":"Alert Data",
                "downlink_type":downlink_type,   
                "alerttype":alert_type_value, 
                "battery_level":low_battery_level,
                "low_battery_level":low_battery_level,
                "alert_temperature":alert_temperature(value),
                "alert_humidity":alert_humidity(value),
                "motion_sensor":alert_motion_start(value),
                "tilt":alert_tilt(value),
                "fall_detection":alert_fall_detetion(value),
                "theft":alert_theft(value),
                "mac_time":mac_time_value,
                'old_position':None,
                'new_position':None,
                "temperature_sign":temperature_sign,
                "temperature":temperature,

            }
            return pay_load
        
        else:
            pay_load={
                "type":"Alert Data",
                "downlink_type":downlink_type,   
                "alerttype":alert_type_value, 
                "battery_level":low_battery_level,
                "low_battery_level":low_battery_level,
                "alert_temperature":alert_temperature(value),
                "alert_humidity":alert_humidity(value),
                "motion_sensor":alert_motion_start(value),
                "tilt":alert_tilt(value),
                "fall_detection":alert_fall_detetion(value),
                "theft":alert_theft(value),
                "mac_time":mac_time_value,
                'old_position':None,
                'new_position':None,
                "temperature_sign":temperature_sign,
                "temperature":temperature,

            }
            return pay_load
    



# print(device_information_EPROM('00000110'))

def googleLatLon(latitude,longitude):
    geocode_result = gmaps.reverse_geocode((latitude, longitude))
    address = geocode_result[0]['formatted_address']
    return address