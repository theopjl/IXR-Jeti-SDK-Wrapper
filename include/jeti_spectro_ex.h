/*----------------------------------------------------------------------------------*/
/*																					*/
/* FILE:    jeti_spectro_ex.h														*/
/* VERSION:	4.8.10																	*/
/*																					*/
/* PURPOSE: This is the header file for jeti_spectro_ex.dll. It is used by the		*/
/*          calling project to gain access to the library functions					*/
/*																					*/
/*			It is not allowed to change or add code here!							*/
/*																					*/
/*			Copyright (C) 2025 by JETI Technische Instrumente GmbH					*/
/*----------------------------------------------------------------------------------*/

#if !defined _USRDLL
#if defined __cplusplus
extern "C" {
#endif
#endif

DWORD __stdcall JETI_GetNumSpectroEx (DWORD *dwNumDevices);
DWORD __stdcall JETI_GetSerialSpectroEx (DWORD dwDeviceNum, char *cBoardSerialNr, char *cSpecSerialNr, char *cDeviceSerialNr);
DWORD __stdcall JETI_OpenSpectroEx (DWORD dwDeviceNum, DWORD_PTR *dwDevice);
DWORD __stdcall JETI_CloseSpectroEx (DWORD_PTR dwDevice);
DWORD __stdcall JETI_StartDarkEx(DWORD_PTR dwDevice, FLOAT fTint, WORD wAver);
DWORD __stdcall JETI_DarkPixEx (DWORD_PTR dwDevice, INT32 *iDark);
DWORD __stdcall JETI_DarkWaveEx (DWORD_PTR dwDevice, DWORD dwBeg, DWORD dwEnd, FLOAT fStep, FLOAT *fDark);
DWORD __stdcall JETI_StartLightEx(DWORD_PTR dwDevice, FLOAT fTint, WORD wAver);
DWORD __stdcall JETI_PrepareLightEx (DWORD_PTR dwDevice, FLOAT fTint, WORD wAver);
DWORD __stdcall JETI_LightPixEx (DWORD_PTR dwDevice, INT32 *iLight);
DWORD __stdcall JETI_LightWaveEx (DWORD_PTR dwDevice, DWORD dwBeg, DWORD dwEnd, FLOAT fStep, FLOAT *fLight);
DWORD __stdcall JETI_StartReferEx (DWORD_PTR dwDevice, FLOAT fTint, WORD wAver);
DWORD __stdcall JETI_PrepareReferEx (DWORD_PTR dwDevice, FLOAT fTint, WORD wAver);
DWORD __stdcall JETI_ReferPixEx (DWORD_PTR dwDevice, INT32 *iRefer);
DWORD __stdcall JETI_ReferWaveEx (DWORD_PTR dwDevice, DWORD dwBeg, DWORD dwEnd, FLOAT fStep, FLOAT *fRefer);
DWORD __stdcall JETI_StartTransReflEx (DWORD_PTR dwDevice, FLOAT fTint, WORD wAver);
DWORD __stdcall JETI_PrepareTransReflEx (DWORD_PTR dwDevice, FLOAT fTint, WORD wAver);
DWORD __stdcall JETI_TransReflPixEx (DWORD_PTR dwDevice, INT32 *iTransRefl);
DWORD __stdcall JETI_TransReflWaveEx (DWORD_PTR dwDevice, DWORD dwBeg, DWORD dwEnd, FLOAT fStep, FLOAT *fTransRefl);
DWORD __stdcall JETI_StartDarkImageEx (DWORD_PTR dwDevice, FLOAT fTint);
DWORD __stdcall JETI_DarkImageEx(DWORD_PTR dwDevice, WORD *wDarkImage);
DWORD __stdcall JETI_StartLightImageEx(DWORD_PTR dwDevice, FLOAT fTint);
DWORD __stdcall JETI_LightImageEx(DWORD_PTR dwDevice, WORD *wLightImage);
DWORD __stdcall JETI_StartChannelDarkEx(DWORD_PTR dwDevice, FLOAT fTint, WORD wAver);
DWORD __stdcall JETI_ChannelDarkEx(DWORD_PTR dwDevice, WORD *wDark);
DWORD __stdcall JETI_StartChannelLightEx(DWORD_PTR dwDevice, FLOAT fTint, WORD wAver);
DWORD __stdcall JETI_ChannelLightEx(DWORD_PTR dwDevice, WORD *wLight);
DWORD __stdcall JETI_StartContDarkEx(DWORD_PTR dwDevice, FLOAT fInterval, DWORD dwCount);
DWORD __stdcall JETI_ContDarkEx(DWORD_PTR dwDevice, WORD *wDark);
DWORD __stdcall JETI_StartContLightEx(DWORD_PTR dwDevice, FLOAT fInterval, DWORD dwCount);
DWORD __stdcall JETI_ContLightEx(DWORD_PTR dwDevice, WORD *wLight);
DWORD __stdcall JETI_StartContChannelDarkEx(DWORD_PTR dwDevice, FLOAT fInterval, DWORD dwCount);
DWORD __stdcall JETI_ContChannelDarkEx(DWORD_PTR dwDevice, WORD *wDark);
DWORD __stdcall JETI_StartContChannelLightEx(DWORD_PTR dwDevice, FLOAT fInterval, DWORD dwCount);
DWORD __stdcall JETI_ContChannelLightEx(DWORD_PTR dwDevice, WORD *wLight);
DWORD __stdcall JETI_SpectroStatusEx (DWORD_PTR dwDevice, BOOL *boIsBusy);
DWORD __stdcall JETI_SpectroBreakEx (DWORD_PTR dwDevice);
DWORD __stdcall JETI_PixelCountEx (DWORD_PTR dwDevice, DWORD *dwPixel);
DWORD __stdcall JETI_SpectroTintEx (DWORD_PTR dwDevice, FLOAT *fTint);
DWORD __stdcall JETI_GetSpectroExDLLVersion (WORD *wMajorVersion, WORD *wMinorVersion, WORD *wBuildNumber);


#if !defined _USRDLL
#if defined __cplusplus
}
#endif
#endif


/*  DLL error codes  */

#define	JETI_SUCCESS				0x00000000		// no error occured
#define JETI_ERROR_OPEN				0x00000001		// device already open
#define JETI_ERROR_OPEN_PORT		0x00000002		// could not open COM-port
#define JETI_ERROR_PORT_SETTING		0x00000003		// could not set COM-port settings
#define JETI_ERROR_BUFFER_SIZE		0x00000004		// could not set buffer size of COM-port
#define JETI_ERROR_PURGE			0x00000005		// could not purge buffers of COM-port
#define JETI_ERROR_TIMEOUT_SETTING	0x00000006		// could not set COM-port timeout
#define JETI_ERROR_SEND				0x00000007		// could not send to device
#define JETI_TIMEOUT				0x00000008		// timeout error
#define JETI_BREAK					0x00000009		// break
#define JETI_ERROR_RECEIVE			0x0000000A		// could not receive from device
#define JETI_ERROR_NAK				0x0000000B		// command not supported or invalid argument
#define JETI_ERROR_CONVERT			0x0000000C		// could not convert received data
#define JETI_ERROR_PARAMETER		0x0000000D		// invalid argument
#define JETI_BUSY					0x0000000E		// device busy
#define JETI_CHECKSUM_ERROR			0x00000011		// invalid checksum of received data
#define JETI_INVALID_STEPWIDTH		0x00000012		// invalid stepwidth
#define JETI_INVALID_NUMBER			0x00000013		// invalid device number
#define JETI_NOT_CONNECTED			0x00000014		// device not connected
#define JETI_INVALID_HANDLE			0x00000015		// invalid device handle
#define JETI_INVALID_CALIB			0x00000016		// invalid calibration file number
#define JETI_CALIB_NOT_READ			0x00000017		// calibration data not read
#define JETI_OVEREXPOSURE			0x00000020		// overexposure
#define JETI_MEASURE_FAIL			0x00000022		// measurement failed
#define JETI_ADAPTION_FAIL			0x00000023		// adaption failed
#define JETI_FILE_NOT_FOUND			0x00000050		// straylight file not found
#define JETI_NO_SLM_DIR				0x00000051		// could not find or create straylight directory
#define JETI_NO_STRAYLIGHT			0x00000052		// no straylight file
#define JETI_NO_MEM					0x00000053		// not enough memory for straylight matrix
#define JETI_NO_SN					0x00000054		// could not read serial number
#define JETI_DLL_ERROR				0x00000080		// internal DLL error
#define JETI_FATAL_ERROR			0x000000FF		// fatal communication error
