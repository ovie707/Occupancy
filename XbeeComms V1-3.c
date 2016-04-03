/*
Ovie Onoriose

XbeeComms V1.3

Trying out API mode with xBees

Replacing timer, which sends grideye data on an interval, with pin interrupts
Adds functionality to receive requests for grid eye data using pin interrupts from the Xbee's digital outputs
*/

//includes
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include "inc/tm4c123gh6pm.h"
#include "inc/hw_memmap.h"
#include "inc/hw_types.h"
#include "driverlib/ssi.h"
#include "driverlib/sysctl.h"
#include "driverlib/interrupt.h"
#include "driverlib/gpio.h"
#include "driverlib/timer.h"
#include "driverlib/pin_map.h"
#include "driverlib/uart.h"
#include "utils/uartstdio.h"

//function prototypes
void init_trigger(void); // enables pin interupt so Rpi can request data through the xbee digital output using remote at command
void init_UART(int choice); // enables uart
void grideye_data(void); // creates dummy grideye data
void send_grideye_packet(char *data, int data_sum); // sends grideye data out the uart in API transmit request format to go to Rpi

//variables
uint8_t ui8PinData=2;
int sys_clock, i;
#define TIMER_FREQ 3
#define UART_BAUDRATE 115200

int main(void)
{
	// Sets the system clock to run using a 16 MHz crystal on the main oscillator to drive the 400 MHz PLL.
	SysCtlClockSet(SYSCTL_SYSDIV_5|SYSCTL_USE_PLL|SYSCTL_XTAL_16MHZ|SYSCTL_OSC_MAIN);
	sys_clock = SysCtlClockGet();

	IntMasterEnable();

	init_trigger();
	init_UART(1); //set to 1 for xBee output //set to 0 for Putty output

	// Enables GPIO port F
	SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF);
	GPIOPinTypeGPIOOutput(GPIO_PORTF_BASE, GPIO_PIN_1|GPIO_PIN_2|GPIO_PIN_3);


	while(1){}
}


void init_trigger(void);
{
	// Enable and configure PE4 as digital input
	SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOE);
	GPIOPinTypeGPIOInput(GPIO_PORTE_BASE, GPIO_PIN_4);
	GPIOIntTypeSet(GPIO_PORTE_BASE, GPIO_PIN_4, GPIO_RISING_EDGE);
	GPIOIntRegister(GPIO_PORTE_BASE, grideye_data);
	IntEnable(INT_GPIOE_TM4C123);
	GPIOIntEnable(GPIO_PORTE_BASE, GPIO_INT_PIN_4);
}


void init_UART(int choice)
{
	if (choice == 1)
	{
		//UART outputs using the following pins
		//PB0 is Launchpad input
		//PB1 is Launchpad output
		SysCtlPeripheralEnable(SYSCTL_PERIPH_UART1);
		SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOB);
		GPIOPinConfigure(GPIO_PB0_U1RX);
		GPIOPinConfigure(GPIO_PB1_U1TX);
		GPIOPinTypeUART(GPIO_PORTB_BASE, GPIO_PIN_0 | GPIO_PIN_1);
		UARTStdioConfig(1, UART_BAUDRATE, sys_clock);
	}
	else
	{
		// UART outputs over USB to Putty
		SysCtlPeripheralEnable(SYSCTL_PERIPH_UART0);
		SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOA);
		GPIOPinConfigure(GPIO_PA0_U0RX);
		GPIOPinConfigure(GPIO_PA1_U0TX);
		GPIOPinTypeUART(GPIO_PORTA_BASE, (GPIO_PIN_0 | GPIO_PIN_1));
		UARTStdioConfig(0, UART_BAUDRATE, sys_clock);
	}
}

void grideye_data(void)
{
	GPIOIntClear(GPIO_PORTE_BASE, GPIO_PIN_4);
//	GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_1|GPIO_PIN_2|GPIO_PIN_3, ui8PinData);
//	SysCtlDelay(1000);
//	GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_1|GPIO_PIN_2|GPIO_PIN_3, 0x00);
//	SysCtlDelay(2000000);

	//this packet sends test from coordinator to router
//	char packet[] = {0x7E, 0x00, 0x12, 0x10, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFE, 0x00, 0x00, 0x74, 0x65, 0x73, 0x74, 0x33};

	//this packet sends test from router to coordinator
//	char packet[] = {0x7E, 0x00, 0x12, 0x10, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0xFE, 0x00, 0x00, 't', 'e', 's', 't', 0x31}; //22 total bytes

//	for(i = 0; i < sizeof(packet); i++)
//		UARTCharPut(UART1_BASE, packet[i]);

	char grideye[] = {5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,\
			5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,\
			5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,\
			5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5};

//	for(i = 0; i < 128; i++)
//	{
//		UARTCharPut(UART0_BASE, grideye[i]);
//	}

	send_grideye_packet(grideye, 0x1A80);
}

void send_grideye_packet(char *data, int data_sum) //data should be 128 bytes long
{
	//  Data comes in as 128 byte char array (each temp register has a high and a low)
	//	Use code below to parse on receiving end to get full temp value
	//	temp[i] = high byte[i]
	//	temp << 8;    /* redundant on first loop */
	//	temp[i] += low byte[i];

	//	packet needs to contain:
	//	xbee frame stuff 17 bytes
	//	unit identifier 1 byte
	//	data type 1 byte
	//	data 128 bytes for grid eye
	//	terminator 2 bytes (0xDF, 0xDF or 223,223)
	//	xbee frame checksum 1 byte

	//initalizing array to beginning of xbee frame (doesn't include RF data or chksum)
	char packet[150] = {0x7E, 0x00, 0x92, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0xFE, 0x00, 0x00};
	int i;

	packet[17] = 0x01; //unit identifier: this unit is #1

	packet[18] = 0x01; //data type: grid eye data is type 1

	//appending RF data into packet
	for(i = 0; i < 128; i++)
	{
		packet[19 + i] = *data;
		data++;
	}

	//RF data terminators for parsing on receiving end
	packet[147] = 0xDF;
	packet[148] = 0xDF;

	//	calculating check sum
	//	xbeeframe data sums up to 0x20E
	//	unit id, data type, and terminator sums to 0x1C0
	//	total sum excluding rf data: 0x3CE
	//	total sum including all 53 rf data: 0x1E4E
	int sum = data_sum + 0x3CE;
	packet[149] = (0xFF - (sum & 0xFF));
	for(i = 0; i < 150; i++)
	{
		UARTCharPut(UART1_BASE,packet[i]);
	}

}
