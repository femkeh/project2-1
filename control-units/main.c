/*
 * GccApplication6.c
 *
 * Created: 3-11-2016 16:46:41
 *  Author: 
 */

 // Set light limit doet et niet, moet tussen de 0 - 255 zijn, maar is niet reeel. Hoe kan dat groter?
 // + alle limits worden niet opgeslagen, als connectie weg is, is de change ook weg. 

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
uint8_t _tempLimit = 169;

uint16_t _lightLimit = 300;

uint8_t _maxDownLimit = 200;

uint8_t _minDownLimit = 5;

uint8_t _state = 0; //ROLLED_DOWN

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
    //uint8_t temp = getAdcValue(1);
    // return tempLimit; 
    uart_putByte(_tempLimit);
}

void getLight() {
    uint16_t light = getAdcValue(0);
    // return light;
    //uart_putByte(0xff); // MOET DIT?
    uart_putDouble(light);
}

void getLightLimit() {
    //uint8_t temp = getAdcValue(1);
    // return tempLimit; 
    //uart_putByte(0xff); // MOET DIT?
    uart_putDouble(_lightLimit);
}

void getMaxDownLimit() {
    //uint8_t temp = getAdcValue(1);
    // return tempLimit; 
    uart_putByte(_maxDownLimit);
}

void getMinDownLimit() {
    //uint8_t temp = getAdcValue(1);
    // return tempLimit; 
    uart_putByte(_minDownLimit);
}

void getCurrentState() {
    //uint8_t temp = getAdcValue(1);
    // return tempLimit; 
    uart_putByte(_state);
}

//----Set functions----
void setTempLimit() {
    //uint8_t temp = getAdcValue(1);
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
    //uint8_t temp = getAdcValue(1);
    // set max roll down Limit; 
    _maxDownLimit = uart_getByte();
      if (_maxDownLimit <= 0) {
        uart_putByte(2);
      } else {
        uart_putByte(12);
      }
}

void setMinDownLimit() {
    //uint8_t temp = getAdcValue(1);
    // set max roll down Limit; 
    _minDownLimit = uart_getByte();
      if (_minDownLimit <= 0) {
        uart_putByte(2);
      } else {
        uart_putByte(12);
      }
}

void setStateRollDown() {
    //uint8_t temp = getAdcValue(1);
    // set max roll down Limit; 
    _state = 0;
}

void setStateRollUp() {
    //uint8_t temp = getAdcValue(1);
    // set max roll down Limit; 
    _state = 1;
}




int main(void) {
	uart_init();
    adc_init();
    SCH_Init_T1();
    SCH_Start();

    // Enable the USART Recieve Complete interrupt (USART_RXC)
    UCSR0B |= (1 << RXCIE0);

    // test ADC
    // SCH_Add_Task(getTemp, 0, 50);
    // SCH_Add_Task(getLight, 0, 100);

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
        //uart_putByte(12);
        setTempLimit(); 
        break;

        case 42:
        // setLightLimit
        //uart_putByte(12);
        setLightLimit(); 
        break;

        case 43:
        // setMaxDownLimit
        //uart_putByte(12);
        setMaxDownLimit(); 
        break;

        case 44:
        // setMinDownLimit
        //uart_putByte(12);
        setMinDownLimit(); 
        break;

        case 45:
        // set state roll down
        //uart_putByte(12);
        setStateRollDown(); 
        uart_putByte(12);
        break;

        case 46:
        // set state roll down
        //uart_putByte(12);
        setStateRollUp(); 
        uart_putByte(12);
        break;

  }
}
