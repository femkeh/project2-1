/*
 * GccApplication6.c
 *
 * Created: 3-11-2016 16:46:41
 *  Author: 
 */

 // Set light limit doet et niet, moet tussen de 0 - 255 zijn, maar is niet reeel. Hoe kan dat groter?

#define F_CPU 16000000UL
#define BAUD 19200

#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/setbaud.h>
#include <util/delay.h>
#include <stdio.h>
#include <avr/sfr_defs.h>
#include "AVR_TTC_scheduler.h"

#define low(x)   ((x) & 0xFF)
#define high(x)   (((x)>>8) & 0xFF)

// Global variables, maar gehardcode dus als setters gebruikt worden dan is dat alleen in zelfde connectie, wordt niet opgeslagen
uint8_t _tempLimit = 174;

uint16_t _lightLimit = 300;

uint8_t _maxDownLimit = 100;

uint8_t _minDownLimit = 5;

uint8_t _currentMode = 0; // not manual

uint8_t _state = 1; //ROLLED_UP = 1, ROLLED_DOWN = 0

int adc_value;        // Variable used to store the value read from the ADC converter

void uart_init(void) {
	UBRR0H = UBRRH_VALUE;
	UBRR0L = UBRRL_VALUE;
	UCSR0A =0;
	UCSR0C = _BV(UCSZ01) | _BV(UCSZ00); /* 8-bit data */
	UCSR0B = _BV(RXEN0) | _BV(TXEN0);   /* Enable RX and TX */
}

void uart_putByte(uint8_t c) {
    loop_until_bit_is_set(UCSR0A, UDRE0); /* Wait until data register empty. */
    UDR0 = c;
}

void uart_putDouble(uint16_t word) {
	uart_putByte(high(word));
    uart_putByte(low(word));
}

char uart_getByte() {
    loop_until_bit_is_set(UCSR0A, RXC0); /* Wait until data exists. */
    return UDR0;
}

void adc_init() {
    ADCSRA |= ((1<<ADPS2)|(1<<ADPS1)|(1<<ADPS0));   // setups up ADC clock prescalar to 128
    ADMUX |= (1<<REFS0);                            // set ref voltage to AVCC
    ADCSRA |= (1<<ADEN);                            // ADC Enable

    ADCSRA |= (1<<ADSC);                            // start sampling                       // start sampling
}

void init_ports() {
    DDRD = 0xff; // set port D as output
    PORTD = 0x00; // LEDs off
}

uint16_t getAdcValue(uint8_t channel) {
    // Returns 8 bit reading (left justified)
        uint16_t adcVal = 0;
        ADMUX &= ~((1<<MUX3)|(1<<MUX2)|(1<<MUX1)|(1<<MUX0)); // Clear ADC Mux Bits
        // read from channel [PC1, A1]
            ADMUX |= channel;                             // setup ADC Channel 1
            ADCSRA |= (1 << ADSC);                          // Start a new conversion,
            while(ADCSRA & _BV(ADSC));                      // Wait until conversion is complete and ADSC is cleared
            return ADCW;                                   // 8 bit reading, ADLAR set
}

//----Get functions----
void getTemp() {
    uint8_t temp = getAdcValue(1);
    // return temp;
    uart_putByte(temp);
}

void getTempLimit() {
    uart_putByte(_tempLimit);
}

void getLight() {
    uint16_t light = getAdcValue(0);
    uart_putDouble(light);
}

void getLightLimit() {
    uart_putDouble(_lightLimit);
}

void getMaxDownLimit() {
    uart_putByte(_maxDownLimit);
}

void getMinDownLimit() {
    uart_putByte(_minDownLimit);
}

void getCurrentState() {
    uart_putByte(_state);
}

//----Set functions----
void setTempLimit() {
    // set tempLimit; 
    _tempLimit = uart_getByte();
      if (_tempLimit <= 0) {
        uart_putByte(2);
      } else {
        uart_putByte(12);
      }
}

void setLightLimit() {
    // set light limit
    uint8_t msb = uart_getByte();
    _lightLimit = (msb << 8)|uart_getByte();
    uart_putByte(12);
}

void setMaxDownLimit() {
    _maxDownLimit = uart_getByte();
      if (_maxDownLimit <= 0) {
        uart_putByte(2);
      } else {
        uart_putByte(12);
      }
}

void setMinDownLimit() {
    _minDownLimit = uart_getByte();
      if (_minDownLimit <= 0) {
        uart_putByte(2);
      } else {
        uart_putByte(12);
      }
}

void setStateRollDown() {
    _state = 0;
}

void setStateRollUp() {
    _state = 1;
}

void setModeToManual() {
    _currentMode = 1;
}

void setManualToMode() {
    _currentMode = 0;
}

void blinkYellowLed() {
    uint8_t max = _maxDownLimit;
    redLightOff();
    while (max > 0) {
        PORTD |= _BV(PORTD4);// PORTD=0x0f; // LEDs on
        // delay 0.5 sec
        _delay_ms(500);
        PORTD=0x00; // led off
        // delay 0.5 sec
        _delay_ms(500);
        max = max - 10; // remove 10 cms
    }
    if (_state == 0) {
        _state = 1;
        redLightOn();
    } 
    else {
        _state = 0;
        greenLightOn();
    }
}

void redLightOn() {
    PORTD |= _BV(PORTD2);
}

void redLightOff() {
    PORTD=0x00;  // is alle poorten D uit..
}

void greenLightOn() {
    PORTD |= _BV(PORTD3);
}

void greenLightOff() {
    PORTD=0x00;  // is alle poorten D uit..
}

void checkTempLimit() {
    if (getAdcValue(1) >= _tempLimit && _state == 1) {
        blinkYellowLed();
    }
}

void checkLightLimit() {
    if (getAdcValue(0) >= _lightLimit && _state == 1) {
        blinkYellowLed();
    }
}



int main(void) {
	uart_init();
    adc_init();
    init_ports();
    SCH_Init_T1();
    SCH_Start();
    if (_state == 1) {
        redLightOn();
    }
    else {
        greenLightOn();
    }

    // Enable the USART Recieve Complete interrupt (USART_RXC)
    UCSR0B |= (1 << RXCIE0);

    // test ADC
    // SCH_Add_Task(getTemp, 0, 50);
    // SCH_Add_Task(getLight, 0, 100);
    SCH_Add_Task(checkTempLimit, 0, 10);
    SCH_Add_Task(checkLightLimit, 0, 10);

    sei();

    while (1) {
        SCH_Dispatch_Tasks();
        // uart_putByte(0x50);
    }
    return 0;
}

ISR (USART_RX_vect)
{
  char receivedByte;
  receivedByte = uart_getByte(); // Fetch the received byte value into the variable "ByteReceived"
  uint8_t collectMore = 0;


  switch (receivedByte) {
        case 21:
        // getTemperature
        uart_putByte(12);
        getTemp();
        break;

        case 22:
        // getTempLimit
        uart_putByte(12);
        getTempLimit(); 
        break;

        case 23:
        // getLight
        uart_putByte(13); // MOET DIT GEHARDCODE BLIJVEN?
        getLight();
        break;

        case 24:
        // getLightLimit
        uart_putByte(13);
        getLightLimit(); 
        break;

        case 25:
        // getMaxDownLimit
        uart_putByte(12);
        getMaxDownLimit();
        break;

        case 26:
        // getMinDownLimit
        uart_putByte(12);
        getMinDownLimit(); 
        break;

        case 27:
        // getCurrentState
        uart_putByte(12);
        getCurrentState(); 
        break;

        // 41-46
        case 41:
        // setTempLimit
        setTempLimit(); 
        break;

        case 42: ;
        // set light limit
        setLightLimit();
        break;

        case 43:
        // setMaxDownLimit
        setMaxDownLimit(); 
        break;

        case 44:
        // setMinDownLimit
        setMinDownLimit(); 
        break;

        case 45:
        // set state roll down
        setStateRollDown(); 
        redLightOff();
        greenLightOn();
        uart_putByte(12);
        break;

        case 46:
        // set state roll down
        setStateRollUp(); 
        redLightOff();
        redLightOn();
        uart_putByte(12);
        break;

        case 47:
        setModeToManual(); 
        uart_putByte(12);
        break;

        case 48:
        setManualToMode(); 
        uart_putByte(12);
        break;

        case 50:
        blinkYellowLed(); 
        break;

  }
}
