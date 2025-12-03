/*---------------------------------------------------------------------------*/
/*                                                                           */
/* FILE:    jeti_radio_ex.h													 */
/* VERSION:	4.8.10															 */
/*                                                                           */
/* PURPOSE: This is the header file for jeti_radio_ex.dll. It is used by the */
/*          calling project to gain access to the library functions			 */
/*																			 */
/*			It is not allowed to change or add code here!					 */
/*                                                                           */
/*			Copyright (C) 2025 by JETI Technische Instrumente GmbH			 */
/*---------------------------------------------------------------------------*/

#if !defined _USRDLL
#if defined __cplusplus
extern "C" {
#endif
#endif

DWORD __stdcall JETI_GetNumRadioEx (DWORD *dwNumDevices);
DWORD __stdcall JETI_GetSerialRadioEx (DWORD dwDeviceNum, char *cBoardSerialNr, char *cSpecSerialNr, char *cDeviceSerialNr);
DWORD __stdcall JETI_OpenRadioEx (DWORD dwDeviceNum, DWORD_PTR *dwDevice);
DWORD __stdcall JETI_CloseRadioEx (DWORD_PTR dwDevice);
DWORD __stdcall JETI_MeasureEx (DWORD_PTR dwDevice, FLOAT fTint, WORD wAver, DWORD dwStep);
DWORD __stdcall JETI_MeasureAdaptEx (DWORD_PTR dwDevice, WORD wAver, DWORD dwStep);
DWORD __stdcall JETI_PrepareMeasureEx (DWORD_PTR dwDevice, FLOAT fTint, WORD wAver, DWORD dwStep);
DWORD __stdcall JETI_MeasureStatusEx (DWORD_PTR dwDevice, BOOL *boStatus);
DWORD __stdcall JETI_MeasureAdaptStatusEx (DWORD_PTR dwDevice, FLOAT *fTint, WORD *wAverage, BOOL *boStatus);
DWORD __stdcall JETI_MeasureBreakEx (DWORD_PTR dwDevice);
DWORD __stdcall JETI_SpecRadEx (DWORD_PTR dwDevice, DWORD dwBeg, DWORD dwEnd, FLOAT *fSprad);
DWORD __stdcall JETI_SpecRadHiResEx(DWORD_PTR dwDevice, DWORD dwBeg, DWORD dwEnd, FLOAT* fSprad);
DWORD __stdcall JETI_SaveSpecRadSPCEx (DWORD_PTR dwDevice, DWORD dwBeg, DWORD dwEnd, char *cPathName, char *cOperator, char *cMemo);
DWORD __stdcall JETI_SaveSpecRadCSVEx (DWORD_PTR dwDevice, DWORD dwBeg, DWORD dwEnd, char *cPathName, char *cOperator, char *cMemo);
DWORD __stdcall JETI_RadioEx (DWORD_PTR dwDevice, DWORD dwBeg, DWORD dwEnd, FLOAT *fRadio);
DWORD __stdcall JETI_PhotoEx (DWORD_PTR dwDevice, FLOAT *fPhoto);
DWORD __stdcall JETI_ChromxyEx (DWORD_PTR dwDevice, FLOAT *fChromx, FLOAT *fChromy);
DWORD __stdcall JETI_Chromxy10Ex (DWORD_PTR dwDevice, FLOAT *fChromx10, FLOAT *fChromy10);
DWORD __stdcall JETI_ChromuvEx (DWORD_PTR dwDevice, FLOAT *fChromu, FLOAT *fChromv);
DWORD __stdcall JETI_ChromXYZEx (DWORD_PTR dwDevice, FLOAT *fX, FLOAT *fY, FLOAT *fZ);
DWORD __stdcall JETI_DWLPEEx (DWORD_PTR dwDevice, FLOAT *fDWL, FLOAT *fPE);
DWORD __stdcall JETI_CCTEx (DWORD_PTR dwDevice, FLOAT *fCCT);
DWORD __stdcall JETI_DuvEx (DWORD_PTR dwDevice, FLOAT *fDuv);
DWORD __stdcall JETI_CRIEx (DWORD_PTR dwDevice, FLOAT fCCT, FLOAT *fCRI);
DWORD __stdcall JETI_TM30Ex (DWORD_PTR dwDevice, BYTE bUseTM3015, DOUBLE* dRf, DOUBLE* dRg, DOUBLE* dChroma, DOUBLE* dHue, DOUBLE* dRfi, DOUBLE* dRfces);
DWORD __stdcall JETI_PeakFWHMEx(DWORD_PTR dwDevice, FLOAT fThreshold, FLOAT* fPeak, FLOAT* fFWHM);
DWORD __stdcall JETI_BlueMeasurementEx(DWORD_PTR dwDevice, FLOAT* fLb, FLOAT* fKbv, FLOAT* fKc, FLOAT* fRbpfs, FLOAT* fRlbtb, FLOAT* fRnbpbp);
DWORD __stdcall JETI_RadioTintEx (DWORD_PTR dwDevice, FLOAT *fTint);
DWORD __stdcall JETI_SetMeasDistEx (DWORD_PTR dwDevice, DWORD dwDistance);
DWORD __stdcall JETI_GetMeasDistEx (DWORD_PTR dwDevice, DWORD *dwDistance);
DWORD __stdcall JETI_GetRadioExDLLVersion (WORD *wMajorVersion, WORD *wMinorVersion, WORD *wBuildNumber);

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
