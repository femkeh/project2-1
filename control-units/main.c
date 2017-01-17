/*
 * GccApplication6.c
 *
 * Created: 3-11-2016 16:46:41
 *  Author:
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

// Global variables, maar gehardcode dus als setters gebruikt worden dan is dat alleen in zelfde connectie, wordt niet opgeslagen
uint8_t _tempLimit = 174;

uint16_t _lightLimit = 500;

uint8_t _blinking = 0;

uint16_t _maxDownLimit = 400; // 100cm = 100 / 15 * 60

uint16_t _minDownLimit = 40; // 10cm = 10 / 15 * 60

uint8_t _currentMode = 0; // not manual = 0, manual = 1

uint8_t _state = 1; //ROLLED_UP = 1, ROLLED_DOWN = 0

int adc_value;        // Variable used to store the value read from the ADC converter

uint16_t _distanceValue = 0; // distancesensor last measurement
volatile uint16_t _gv_counter; // 16 bit
volatile uint8_t _echo; // a flag

void checkDistanceMeter();

void uart_init(void) {
	UBRR0H = UBRRH_VALUE;
	UBRR0L = UBRRL_VALUE;
	UCSR0A =0;
	UCSR0C = _BV(UCSZ01) | _BV(UCSZ00); // 8-bit data 
	UCSR0B = _BV(RXEN0) | _BV(TXEN0);   // Enable RX and TX 
}

void uart_putByte(uint8_t c) {
    loop_until_bit_is_set(UCSR0A, UDRE0); // Wait until data register empty
    UDR0 = c;
}

void uart_putDouble(uint16_t word) {
	uart_putByte(high(word));
    uart_putByte(low(word));
}

char uart_getByte() {
    loop_until_bit_is_set(UCSR0A, RXC0); // Wait until data exists 
    return UDR0;
}

void adc_init() {
    ADCSRA |= ((1<<ADPS2)|(1<<ADPS1)|(1<<ADPS0));   // setups up ADC clock prescalar to 128
    ADMUX |= (1<<REFS0);                            // set ref voltage to AVCC
    ADCSRA |= (1<<ADEN);                            // ADC Enable

    ADCSRA |= (1<<ADSC);                            // start sampling                       
}

void init_ports() {
    DDRB = 0xff; // set port B as output
    PORTB = 0x00; // LEDs off
    DDRD &= ~(1 << PIND3);
	DDRD |= (1 << PIND2);
    PORTD = 0x00;
    _delay_us(2);
}

void init_timer(void)
// prescale, no interrupt, counting up
{
    // prescaling : max time = 2^16/16E6 = 4.1 ms, 4.1 >> 2.3, so no prescaling required
    TCCR1A = 0;
    TCCR1B = _BV(CS10);
}

void init_ext_int(void)
{
    // any change triggers ext interrupt 1
    EICRA = (1 << ISC10);
    EIMSK = (1 << INT1);
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
    uart_putDouble(_maxDownLimit);
}

void getMinDownLimit() {
    uart_putDouble(_minDownLimit);
}

void getCurrentState() {
    // _delay_ms()
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
    uint8_t msb = uart_getByte();
    _maxDownLimit = (msb << 8)|uart_getByte();
      if (_maxDownLimit <= 0) {
        uart_putByte(2);
      } else {
        uart_putByte(11);
      }
}

void setMinDownLimit() {
    uint8_t msb = uart_getByte();
    _minDownLimit = (msb << 8)|uart_getByte();
      if (_minDownLimit <= 0) {
        uart_putByte(2);
      } else {
        uart_putByte(11);
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
    _blinking = 1; // true
}

void redLightOn() {
    PORTB |= _BV(PORTB0);
}

void redLightOff() {
    PORTB=0x00;  // is alle poorten D uit..
}

void greenLightOn() {
    PORTB |= _BV(PORTB1);
}

void greenLightOff() {
    PORTB=0x00;  // is alle poorten D uit..
}

void checkTempLimit() {
    if (_currentMode == 0) {
        if (getAdcValue(1) >= _tempLimit && _state == 1) {
            blinkYellowLed();
        }
    }
}

void checkLightLimit() {
    if (_currentMode == 0) {
        if (getAdcValue(0) >= _lightLimit && _state == 1) {
            blinkYellowLed();
        }
    }
}

void checkDistanceMeter() {
    _echo = 0x1; // set flag
    // start trigger puls lo -> hi
    PORTD |= _BV(PIND2); // set bit D2
    _delay_us(12); // micro sec
    PORTD &=~ _BV(PIND2); // clear bit D2
    _delay_ms(20); // milli sec, timer1 is read in ISR
    _distanceValue = _gv_counter;
    _delay_ms(10);
}

void getCurrentDistance() {
    uart_putDouble(_distanceValue);
}

int main(void) {
	uart_init();
    adc_init();

    init_ports();
    init_ext_int();
    init_timer();

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
    SCH_Add_Task(checkDistanceMeter, 0, 50);

    sei();
    while (1) {
        SCH_Dispatch_Tasks();
        if (_blinking) {
            redLightOff();

            if (_state == 0) {
                while (_distanceValue >= (_maxDownLimit - _minDownLimit)) {
                    PORTB |= _BV(PORTB2);// PORTB=0x0f; // LEDs on
                    // delay 0.5 sec
                    _delay_ms(500);
                    PORTB=0x00; // led off
                    // delay 0.5 sec
                    _delay_ms(500);
                    checkDistanceMeter();
                }
                _state = 1;
                redLightOn();
            } else {
                while (_distanceValue >= _minDownLimit) {
                    PORTB |= _BV(PORTB2);// PORTB=0x0f; // LEDs on
                    // delay 0.5 sec
                    _delay_ms(500);
                    PORTB=0x00; // led off
                    // delay 0.5 sec
                    _delay_ms(500);
                    checkDistanceMeter();
                }
                _state = 0;
                greenLightOn();
            }
            _blinking = 0;
        }
    }
    return 0;
}

ISR (INT1_vect)
{
    if (_echo == 0x1) {
        // set timer1 value to zero
        TCNT1 = 0;
        // clear flag
        _echo = 0x0;
    } else {
        // read value timer1
        _gv_counter = TCNT1;
    }
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
        uart_putByte(13);
        getMaxDownLimit();
        break;

        case 26:
        // getMinDownLimit
        uart_putByte(13);
        getMinDownLimit();
        break;

        case 27:
        // getCurrentState
        uart_putByte(12);
        getCurrentState();
        break;

        case 28:
        // getCurrentDistance
        uart_putByte(13);
        getCurrentDistance();
        break;

        case 29:
        // isCurrentlyBlinking
        uart_putByte(12);
        uart_putByte(_blinking);
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
        uart_putByte(11);
        break;

        case 46:
        // set state roll down
        setStateRollUp();
        redLightOff();
        redLightOn();
        uart_putByte(11);
        break;

        case 47:
        setModeToManual();
        uart_putByte(11);
        break;

        case 48:
        setManualToMode();
        uart_putByte(11);
        break;

        case 50:
        blinkYellowLed();
        uart_putByte(11);
        break;

  }
}
