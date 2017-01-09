/*
 * GccApplication6.c
 *
 * Created: 3-11-2016 16:46:41
 *  Author: Simon van der Meer
 */
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

void getLight() {
    uint16_t light = getAdcValue(0);
    // return light;
    uart_putByte(0xff);
    uart_putDouble(0x00);
}

void getTemp() {
    uint8_t temp = getAdcValue(1);
    // return temp;
    uart_putByte(0xfe);
    uart_putByte(temp);
}

int main(void) {
	uart_init();
    adc_init();
    SCH_Init_T1();
    SCH_Start();

    // test ADC
    SCH_Add_Task(getTemp, 0, 50);
    SCH_Add_Task(getLight, 0, 100);

    sei();

    while (1) {
        SCH_Dispatch_Tasks();
        // uart_putByte(0x50);
    }
    return 0;
}
