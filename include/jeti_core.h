/*---------------------------------------------------------------------------*/
/*                                                                           */
/* FILE:    jeti_core.h														 */
/* VERSION:	4.8.10															 */
/*                                                                           */
/* PURPOSE: This is the header file for jeti_core.dll. It is used by the	 */
/*          calling project to gain access to the library functions			 */
/*																			 */
/*			It is not allowed to change or add code here!					 */
/*                                                                           */
/*			Copyright (C) 2025 by JETI Technische Instrumente GmbH			 */
/*---------------------------------------------------------------------------*/

/* DLL-Function Prototypes */

#define WM_JETIENQUIRY	0x9000

typedef void (__stdcall *vCallbackFunction) (void); 


#if !defined _USRDLL
#if defined __cplusplus
extern "C" {
#endif
#endif

DWORD __stdcall JETI_SetLicKey (char* cLicKey);
DWORD __stdcall JETI_ImportSLM (char* cMatrixFile);
DWORD __stdcall JETI_IgnoreSLM (BYTE bIgnore);

// Device Handling
DWORD __stdcall JETI_GetNumDevices (DWORD *dwNumDevices);
DWORD __stdcall JETI_GetSerialDevice (DWORD dwDeviceNum, char *cBoardSerialNr, char *cSpecSerialNr, char *cDeviceSerialNr);
DWORD __stdcall JETI_GetDeviceInfo (DWORD dwDeviceNum, BYTE *bConnType, BYTE *bDeviceType, char *cDeviceSerial, WORD *wComPortNr, DWORD *dwBaudrate, char *cIPAddress, char *cUSBSerial, unsigned long long *btAddress);
DWORD __stdcall JETI_GetDeviceInfoEx (DWORD dwDeviceNum, BYTE* bConnType, BYTE* bDeviceType, char* cDeviceSerial, WORD* wComPortNr, DWORD* dwBaudrate, char* cIPAddress, char* cUSBSerial, unsigned long long* btAddress, WCHAR* wcBTLEDevicePath);
DWORD __stdcall JETI_OpenDevice (DWORD dwDeviceNum, DWORD_PTR *dwDevice);
DWORD __stdcall JETI_OpenCOMDevice (DWORD dwComPort, DWORD dwBaudrate, DWORD_PTR *dwDevice);
DWORD __stdcall JETI_OpenTCPDevice (char * cIPAddr, DWORD_PTR *dwDevice);
DWORD __stdcall JETI_OpenFTDIDevice (char * cUSBSerial, DWORD_PTR *dwDevice);
DWORD __stdcall JETI_OpenBTDevice (unsigned long long btAddress, DWORD_PTR *dwDevice);
DWORD __stdcall JETI_OpenBTLEDevice(WCHAR* wcBTLEDevicePath, DWORD_PTR* dwDevice);
DWORD __stdcall JETI_CloseDevice (DWORD_PTR dwDevice);
DWORD __stdcall JETI_GetIdentifier (DWORD_PTR dwDevice, char *cIdentifier);
DWORD __stdcall JETI_ArbitraryCommand (DWORD_PTR dwDevice, char *cCommand, char *cAnswer);
DWORD __stdcall JETI_DeviceWrite (DWORD_PTR dwDevice, char *cCommand, DWORD dwBytesToWrite, DWORD dwTimeout);
DWORD __stdcall JETI_DeviceRead (DWORD_PTR dwDevice, char *cResponse, DWORD dwBytesToRead, DWORD *dwBytesRead, DWORD dwTimeout);
DWORD __stdcall JETI_DeviceReadTerm (DWORD_PTR dwDevice, char *cResponse, DWORD dwMaxBytes, DWORD dwTimeout);
DWORD __stdcall JETI_DataReceived(DWORD_PTR dwDevice, int iMaxLength);
DWORD __stdcall JETI_Reset (DWORD_PTR dwDevice);
DWORD __stdcall JETI_HardReset (DWORD_PTR dwDevice);
DWORD __stdcall JETI_Break (DWORD_PTR dwDevice);
DWORD __stdcall JETI_InitMeasure (DWORD_PTR dwDevice);
DWORD __stdcall JETI_PreTrigMeasure (DWORD_PTR dwDevice);
DWORD __stdcall JETI_MeasureStatusCore (DWORD_PTR dwDevice, BOOL *boStatus);
DWORD __stdcall JETI_WaitReadTrigger (DWORD_PTR dwDevice, INT32 *iSpec, DWORD dwTimeout);
DWORD __stdcall JETI_StartAdaption (DWORD_PTR dwDevice, BOOL boReference);
DWORD __stdcall JETI_CheckAdaptionStat (DWORD_PTR dwDevice, FLOAT *fTint, WORD *wAverage, BOOL *boStatus);
DWORD __stdcall JETI_ReadCalib (DWORD_PTR dwDevice, DWORD dwCalibNr, char *cMode, char *cRemark, DWORD *dwBegin, DWORD *dwEnd, DWORD *dwStep, DWORD *dwTint, double *dValue);
DWORD __stdcall JETI_WriteCalib (DWORD_PTR dwDevice, DWORD dwCalibNr, char *cMode, char *cRemark, DWORD dwBegin, DWORD dwEnd, DWORD dwStep, DWORD dwTint, double *dValue);
DWORD __stdcall JETI_DeleteCalib (DWORD_PTR dwDevice, DWORD dwCalibNr);
DWORD __stdcall JETI_GetCalibRange (DWORD_PTR dwDevice, DWORD *dwBegin, DWORD *dwEnd, DWORD *dwStep);
DWORD __stdcall JETI_SetCalib (DWORD_PTR dwDevice, BYTE bCalibNr);
DWORD __stdcall JETI_GetCalib (DWORD_PTR dwDevice, BYTE *bCalibNr);
DWORD __stdcall JETI_MeasCompDark (DWORD_PTR dwDevice);
DWORD __stdcall JETI_GetComPortHandle (DWORD_PTR dwDevice, HANDLE* hComPortHandle);
DWORD __stdcall JETI_MeasureADC1 (DWORD_PTR dwDevice, WORD *wADC1);
DWORD __stdcall JETI_MeasureADC2 (DWORD_PTR dwDevice, WORD *wADC2);
DWORD __stdcall JETI_ReadUserData64 (DWORD_PTR dwDevice, BYTE *bData, DWORD dwStart, DWORD dwEnd);
DWORD __stdcall JETI_WriteUserData64 (DWORD_PTR dwDevice, BYTE *bData, DWORD dwBlock);
DWORD __stdcall JETI_GetCoreDLLVersion (WORD *wMajorVersion, WORD *wMinorVersion, WORD *wBuildNumber);
DWORD __stdcall JETI_GetFirmwareVersion (DWORD_PTR dwDevice, char *cVersionString);
DWORD __stdcall JETI_GetDeviceType (DWORD_PTR dwDevice, BYTE *bDeviceType);
DWORD __stdcall JETI_GetBatteryStat (DWORD_PTR dwDevice, float *fBattVolt, BYTE *bBattPercent, BYTE *bIsBattLoading);
DWORD __stdcall JETI_GetLastError (DWORD_PTR dwDevice, DWORD *dwErrorCode);
DWORD __stdcall JETI_GetEnquiry (DWORD_PTR dwDevice, DWORD *dwEnquiry);
DWORD __stdcall JETI_SetCallbackFunction (DWORD_PTR dwDevice, BYTE bEventChar, HWND hMainWnd);

// Parameter functions (jeti_param.c)
DWORD __stdcall JETI_GetPixel (DWORD_PTR dwDevice, DWORD *dwPixel);
DWORD __stdcall JETI_GetPixelBinning (DWORD_PTR dwDevice, BYTE *bPixBin);
DWORD __stdcall JETI_GetFit (DWORD_PTR dwDevice, FLOAT *fFit);
DWORD __stdcall JETI_GetSDelay (DWORD_PTR dwDevice, DWORD *dwSDelay);
DWORD __stdcall JETI_SetSDelay (DWORD_PTR dwDevice, DWORD dwSDelay);
DWORD __stdcall JETI_GetTint (DWORD_PTR dwDevice, float *fTint);
DWORD __stdcall JETI_GetADCRes (DWORD_PTR dwDevice, BYTE *bADCRes);
DWORD __stdcall JETI_GetSplitTime (DWORD_PTR dwDevice, DWORD *dwSplitTime);
DWORD __stdcall JETI_GetBorder (DWORD_PTR dwDevice, BYTE *bBorderMin, BYTE *bBorderMax);
DWORD __stdcall JETI_GetDistance (DWORD_PTR dwDevice, DWORD *dwDistance);
DWORD __stdcall JETI_SetDistance (DWORD_PTR dwDevice, DWORD dwDistance);
DWORD __stdcall JETI_GetParamBlock (DWORD_PTR dwDevice, BYTE *bParam);
DWORD __stdcall JETI_SetParamBlock (DWORD_PTR dwDevice, BYTE *bParam);
DWORD __stdcall JETI_GetOptTrigg (DWORD_PTR dwDevice, BOOL *boOptTrigg);
DWORD __stdcall JETI_SetLaserIntensity (DWORD_PTR dwDevice, DWORD dwIntensity, DWORD dwModulation);
DWORD __stdcall JETI_SetTrigger (DWORD_PTR dwDevice, DWORD dwTriggerMode);
DWORD __stdcall JETI_GetTrigTimeout(DWORD_PTR dwDevice, WORD *wTimeout);
DWORD __stdcall JETI_SetTrigTimeout(DWORD_PTR dwDevice, WORD wTimeout);
DWORD __stdcall JETI_SetFlashMode (DWORD_PTR dwDevice, BOOL boFlashMode);
DWORD __stdcall JETI_SetFlashCycle (DWORD_PTR dwDevice, DWORD dwFlashCycle);
DWORD __stdcall JETI_GetCorrectionStat (DWORD_PTR dwDevice, BOOL *boCorrStat);
DWORD __stdcall JETI_SetCorrectionStat (DWORD_PTR dwDevice, BOOL boCorrStat);
DWORD __stdcall JETI_GetCorrectionRange (DWORD_PTR dwDevice, DWORD *dwCorrStart, DWORD *dwCorrEnd);
DWORD __stdcall JETI_SetCorrectionRange (DWORD_PTR dwDevice, DWORD dwCorrStart, DWORD dwCorrEnd);
DWORD __stdcall JETI_GetOffsetCorrRange (DWORD_PTR dwDevice, DWORD *dwCorrStart, DWORD *dwCorrEnd);
DWORD __stdcall JETI_SetOffsetCorrRange (DWORD_PTR dwDevice, DWORD dwCorrStart, DWORD dwCorrEnd);
DWORD __stdcall JETI_GetCorrectionCoeff (DWORD_PTR dwDevice, FLOAT *fCorrCoeff);
DWORD __stdcall JETI_SetCorrectionCoeff (DWORD_PTR dwDevice, FLOAT *fCorrCoeff);
DWORD __stdcall JETI_GetCutoffStat (DWORD_PTR dwDevice, BOOL *boCutoffStat);
DWORD __stdcall JETI_SetCutoffStat (DWORD_PTR dwDevice, BOOL boCutoffStat);
DWORD __stdcall JETI_GetBaudrate (DWORD_PTR dwDevice, DWORD *dwBaudrate);
DWORD __stdcall JETI_GetSLMEnable (DWORD_PTR dwDevice, BYTE* bSLMEnable);
DWORD __stdcall JETI_SetSLMEnable (DWORD_PTR dwDevice, BYTE bSLMEnable);
DWORD __stdcall JETI_SetChannelConf (DWORD_PTR dwDevice, char *cChannelConf);
DWORD __stdcall JETI_GetChannelConf (DWORD_PTR dwDevice, char *cChannelConf);
DWORD __stdcall JETI_SetLampMode (DWORD_PTR dwDevice, BYTE bLampMode);
DWORD __stdcall JETI_GetLampMode (DWORD_PTR dwDevice, BYTE *bLampMode);
DWORD __stdcall JETI_SetFlash (DWORD_PTR dwDevice, float fInterval, float fPulselen);
DWORD __stdcall JETI_GetFlash (DWORD_PTR dwDevice, float *fInterval, float *fPulselen);

// Control functions (jeti_contr.c)
DWORD __stdcall JETI_GetLaserStat (DWORD_PTR dwDevice, BOOL *boLaserStat);
DWORD __stdcall JETI_SetLaserStat (DWORD_PTR dwDevice, BOOL boLaserStat);
DWORD __stdcall JETI_GetShutterStat (DWORD_PTR dwDevice, BOOL *boShutterStat);
DWORD __stdcall JETI_SetShutterStat (DWORD_PTR dwDevice, BOOL boShutterStat);
DWORD __stdcall JETI_GetMeasHead (DWORD_PTR dwDevice, BYTE *bMeasHead);
DWORD __stdcall JETI_GetAux1Stat (DWORD_PTR dwDevice, BOOL *boAuxStat);
DWORD __stdcall JETI_SetAux1Stat (DWORD_PTR dwDevice, BOOL boAuxStat);
DWORD __stdcall JETI_GetAux2Stat (DWORD_PTR dwDevice, BOOL *boAuxStat);
DWORD __stdcall JETI_SetAux2Stat (DWORD_PTR dwDevice, BOOL boAuxStat);
DWORD __stdcall JETI_AuxOut1 (DWORD_PTR dwDevice, BOOL boAux1);
DWORD __stdcall JETI_AuxOut1Stat (DWORD_PTR dwDevice, BOOL *boAux1Stat);
DWORD __stdcall JETI_AuxOut2 (DWORD_PTR dwDevice, BOOL boAux2);
DWORD __stdcall JETI_AuxOut2Stat (DWORD_PTR dwDevice, BOOL *boAux2Stat);
DWORD __stdcall JETI_AuxOut3 (DWORD_PTR dwDevice, BOOL boAux3);
DWORD __stdcall JETI_AuxOut3Stat (DWORD_PTR dwDevice, BOOL *boAux3Stat);
DWORD __stdcall JETI_AuxOut4 (DWORD_PTR dwDevice, BOOL boAux4);
DWORD __stdcall JETI_AuxOut4Stat (DWORD_PTR dwDevice, BOOL *boAux4Stat);
DWORD __stdcall JETI_AuxOut5 (DWORD_PTR dwDevice, BOOL boAux5);
DWORD __stdcall JETI_AuxOut5Stat (DWORD_PTR dwDevice, BOOL *boAux5Stat);
DWORD __stdcall JETI_AuxIn1Stat (DWORD_PTR dwDevice, BOOL *boAuxIn1Stat);
DWORD __stdcall JETI_AuxIn2Stat (DWORD_PTR dwDevice, BOOL *boAuxIn2Stat);
DWORD __stdcall JETI_GetFlickerFreq (DWORD_PTR dwDevice, float *fFlickerFreq, DWORD *dwWarning);
DWORD __stdcall JETI_SetSyncFreq (DWORD_PTR dwDevice, float fSyncFreq);
DWORD __stdcall JETI_GetSyncFreq (DWORD_PTR dwDevice, float *fSyncFreq);
DWORD __stdcall JETI_SetSyncMode (DWORD_PTR dwDevice, BYTE bSyncMode);
DWORD __stdcall JETI_GetSyncMode (DWORD_PTR dwDevice, BYTE *bSyncMode);
DWORD __stdcall JETI_GetDIOIn (DWORD_PTR dwDevice, BYTE *bDIOIn);
DWORD __stdcall JETI_GetDIOOut (DWORD_PTR dwDevice, BYTE *bDIOOut);
DWORD __stdcall JETI_SetDIOOut (DWORD_PTR dwDevice, BYTE bDIOOut);
DWORD __stdcall JETI_SetDIOOutPin (DWORD_PTR dwDevice, BYTE bPinNr, BOOL boDIOOut);
DWORD __stdcall JETI_GetTemperature (DWORD_PTR dwDevice, FLOAT *fTemperature);

// Configuration functions (jeti_conf.c)
DWORD __stdcall JETI_GetDarkmodeConf (DWORD_PTR dwDevice, BYTE *bDarkmode);
DWORD __stdcall JETI_SetDarkmodeConf (DWORD_PTR dwDevice, BYTE bDarkmode);
DWORD __stdcall JETI_GetExposureConf (DWORD_PTR dwDevice, BYTE *bExpmode);
DWORD __stdcall JETI_SetExposureConf (DWORD_PTR dwDevice, BYTE bExpmode);
DWORD __stdcall JETI_GetFunctionConf (DWORD_PTR dwDevice, BYTE *bPrevFunc, BYTE *bConfFunc);
DWORD __stdcall JETI_SetFunctionConf (DWORD_PTR dwDevice, BYTE bFunction);
DWORD __stdcall JETI_GetFormatConf (DWORD_PTR dwDevice, BYTE *bPrevForm, BYTE *bConfForm);
DWORD __stdcall JETI_SetFormatConf (DWORD_PTR dwDevice, BYTE bFormat);
DWORD __stdcall JETI_GetTintConf (DWORD_PTR dwDevice, float *fPrevTint, float *fConfTint);
DWORD __stdcall JETI_SetTintConf (DWORD_PTR dwDevice, float fTint);
DWORD __stdcall JETI_GetMaxTintConf (DWORD_PTR dwDevice, float *fMaxTint);
DWORD __stdcall JETI_SetMaxTintConf (DWORD_PTR dwDevice, float fMaxTint);
DWORD __stdcall JETI_GetMaxAverConf(DWORD_PTR dwDevice, WORD *wMaxAver);
DWORD __stdcall JETI_SetMaxAverConf(DWORD_PTR dwDevice, WORD wMaxAver);
DWORD __stdcall JETI_GetMinTintConf(DWORD_PTR dwDevice, float *fMinTint);
DWORD __stdcall JETI_GetImageMinTintConf(DWORD_PTR dwDevice, float* fMinTint);
DWORD __stdcall JETI_GetChanMinTintConf(DWORD_PTR dwDevice, float *fMinTint);
DWORD __stdcall JETI_GetContMinTintConf(DWORD_PTR dwDevice, float *fMinTint);
DWORD __stdcall JETI_GetContChanMinTintConf(DWORD_PTR dwDevice, float *fMinTint);
DWORD __stdcall JETI_GetAverConf (DWORD_PTR dwDevice, WORD *wPrevAver, WORD *wConfAver);
DWORD __stdcall JETI_SetAverConf (DWORD_PTR dwDevice, WORD wAver);
DWORD __stdcall JETI_GetAdaptConf (DWORD_PTR dwDevice, BYTE *bAdaptmode);
DWORD __stdcall JETI_SetAdaptConf (DWORD_PTR dwDevice, BYTE bAdaptmode);
DWORD __stdcall JETI_GetWranConf (DWORD_PTR dwDevice, DWORD *dwBeg, DWORD *dwEnd, DWORD *dwStep);
DWORD __stdcall JETI_SetWranConf (DWORD_PTR dwDevice, DWORD dwBeg, DWORD dwEnd, DWORD dwStep);
DWORD __stdcall JETI_GetPDARowConf (DWORD_PTR dwDevice, DWORD *dwPDARow, DWORD *dwRowNumber);
DWORD __stdcall JETI_SetPDARowConf (DWORD_PTR dwDevice, DWORD dwPDARow, DWORD dwRowNumber);
DWORD __stdcall JETI_SetDefault (DWORD_PTR dwDevice);
DWORD __stdcall JETI_GetLevel (DWORD_PTR dwDevice, DWORD *dwLevelCounts, DWORD *dwLevelPercent);

// Fetch functions (jeti_fetch.c)
DWORD __stdcall JETI_FetchDark (DWORD_PTR dwDevice, INT32 *iDark);
DWORD __stdcall JETI_FetchLight (DWORD_PTR dwDevice, INT32 *iLight);
DWORD __stdcall JETI_FetchRefer (DWORD_PTR dwDevice, INT32 *iRefer);
DWORD __stdcall JETI_FetchTransRefl (DWORD_PTR dwDevice, INT32 *iTransRefl);
DWORD __stdcall JETI_FetchSprad (DWORD_PTR dwDevice, FLOAT *fSprad);
DWORD __stdcall JETI_FetchSpradHiRes (DWORD_PTR dwDevice, FLOAT* fSprad);
DWORD __stdcall JETI_FetchRadio (DWORD_PTR dwDevice, FLOAT *fRadio);
DWORD __stdcall JETI_FetchPhoto (DWORD_PTR dwDevice, FLOAT *fPhoto);
DWORD __stdcall JETI_FetchChromxy (DWORD_PTR dwDevice, FLOAT *fChromx, FLOAT *Chromy);
DWORD __stdcall JETI_FetchChromuv (DWORD_PTR dwDevice, FLOAT *fChromu, FLOAT *fChromv);
DWORD __stdcall JETI_FetchDWLPE (DWORD_PTR dwDevice, FLOAT *fDWL, FLOAT *fPE);
DWORD __stdcall JETI_FetchCCT (DWORD_PTR dwDevice, FLOAT *fCCT);
DWORD __stdcall JETI_FetchDuv (DWORD_PTR dwDevice, FLOAT *fDuv);
DWORD __stdcall JETI_FetchCRI (DWORD_PTR dwDevice, FLOAT *fCRI);
DWORD __stdcall JETI_FetchXYZ (DWORD_PTR dwDevice, FLOAT *fX, FLOAT *fY, FLOAT *fZ);
DWORD __stdcall JETI_FetchTiAdapt (DWORD_PTR dwDevice, FLOAT *fTiAdapt);
DWORD __stdcall JETI_FetchAverAdapt (DWORD_PTR dwDevice, WORD *wAverAdapt);

// Calculation functions (jeti_calc.c)
DWORD __stdcall JETI_CalcLintDark (DWORD_PTR dwDevice, DWORD dwBeg, DWORD dwEnd, FLOAT fStep, FLOAT *fDark);
DWORD __stdcall JETI_CalcSplinDark (DWORD_PTR dwDevice, DWORD dwBeg, DWORD dwEnd, FLOAT fStep, FLOAT *fDark);
DWORD __stdcall JETI_CalcLintLight (DWORD_PTR dwDevice, DWORD dwBeg, DWORD dwEnd, FLOAT fStep, FLOAT *fLight);
DWORD __stdcall JETI_CalcSplinLight (DWORD_PTR dwDevice, DWORD dwBeg, DWORD dwEnd, FLOAT fStep, FLOAT *fLight);
DWORD __stdcall JETI_CalcLintRefer (DWORD_PTR dwDevice, DWORD dwBeg, DWORD dwEnd, FLOAT fStep, FLOAT *fRefer);
DWORD __stdcall JETI_CalcSplinRefer (DWORD_PTR dwDevice, DWORD dwBeg, DWORD dwEnd, FLOAT fStep, FLOAT *fRefer);
DWORD __stdcall JETI_CalcLintTransRefl (DWORD_PTR dwDevice, DWORD dwBeg, DWORD dwEnd, FLOAT fStep, FLOAT *fTransRefl);
DWORD __stdcall JETI_CalcSplinTransRefl (DWORD_PTR dwDevice, DWORD dwBeg, DWORD dwEnd, FLOAT fStep, FLOAT *fTransRefl);
DWORD __stdcall JETI_CalcRadio (DWORD_PTR dwDevice, DWORD dwBeg, DWORD dwEnd, FLOAT *fRadio);
DWORD __stdcall JETI_CalcPhoto (DWORD_PTR dwDevice, FLOAT *fPhoto);
DWORD __stdcall JETI_CalcChromxy (DWORD_PTR dwDevice, FLOAT *fChromx, FLOAT *fChromy);
DWORD __stdcall JETI_CalcChromxy10 (DWORD_PTR dwDevice, FLOAT *fChromx, FLOAT *fChromy);
DWORD __stdcall JETI_CalcChromuv (DWORD_PTR dwDevice, FLOAT *fChromu, FLOAT *fChromv);
DWORD __stdcall JETI_CalcDWLPE (DWORD_PTR dwDevice, FLOAT *fDWL, FLOAT *fPE);
DWORD __stdcall JETI_CalcCCT (DWORD_PTR dwDevice, FLOAT *fCCT);
DWORD __stdcall JETI_CalcDuv (DWORD_PTR dwDevice, FLOAT *fDuv);
DWORD __stdcall JETI_CalcCRI (DWORD_PTR dwDevice, FLOAT fCCT, FLOAT *fCRI);
DWORD __stdcall JETI_CalcXYZ (DWORD_PTR dwDevice, FLOAT *fX, FLOAT *fY, FLOAT *fZ);
DWORD __stdcall JETI_CalcAllValue (DWORD_PTR dwDevice, DWORD dwBeg, DWORD dwEnd, FLOAT *fRadio, FLOAT *fPhoto, FLOAT *fChromx, FLOAT *fChromy, FLOAT *fChromu, FLOAT *fChromv, FLOAT *fDWL, FLOAT *fPE);
DWORD __stdcall JETI_CalcTM30 (DWORD_PTR dwDevice, BYTE bUseTM3015, double* dRf, double* dRg, double* dChroma, double* dHue, double* dRfi, double* dRfces);
DWORD __stdcall JETI_CalcPeakFWHM(DWORD_PTR dwDevice, FLOAT fThreshold, FLOAT* fPeak, FLOAT* fFWHM);
DWORD __stdcall JETI_CalcBlueMeasurement(DWORD_PTR dwDevice, FLOAT* fLb, FLOAT* fKbv, FLOAT* fKc, FLOAT* fRbpfs, FLOAT* fRlbtb, FLOAT* fRnbpbp);

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
#define JETI_CALC_ERROR				0x00000081		// calculation error
#define JETI_ERROR_READ				0x00000100		// could not read from COM port
#define JETI_FATAL_ERROR			0x000000FF		// fatal communication error
