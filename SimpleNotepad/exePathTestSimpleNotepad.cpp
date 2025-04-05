#include <windows.h>
#include <commdlg.h>
#include <string>

#define IDM_SAVE 1
#define IDM_LOAD 2

LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam);
void SaveFile(HWND hwndEdit, HWND hwnd);
void LoadFile(HWND hwndEdit, HWND hwnd);

WCHAR filename[MAX_PATH] = L""; // Store the current filename
HWND hwndEdit; // Global handle to edit control

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    // Register window class
    WNDCLASS wc = { 0 };
    wc.lpfnWndProc = WndProc;
    wc.hInstance = hInstance;
    wc.lpszClassName = L"NotepadClass";
    RegisterClass(&wc);

    // Create main window
    HWND hwnd = CreateWindow(L"NotepadClass", L"Simple Notepad", WS_OVERLAPPEDWINDOW,
        CW_USEDEFAULT, CW_USEDEFAULT, 500, 400, NULL, NULL, hInstance, NULL);

    ShowWindow(hwnd, nCmdShow);
    UpdateWindow(hwnd);

    // Message loop
    MSG msg;
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }
    return msg.wParam;
}

LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam) {
    switch (msg) {
    case WM_CREATE: {
        // Create menu
        HMENU hMenu = CreateMenu();
        HMENU hFileMenu = CreateMenu();
        AppendMenu(hFileMenu, MF_STRING, IDM_SAVE, L"Save");
        AppendMenu(hFileMenu, MF_STRING, IDM_LOAD, L"Load");
        AppendMenu(hMenu, MF_POPUP, (UINT_PTR)hFileMenu, L"File");
        SetMenu(hwnd, hMenu);

        // Create edit control
        hwndEdit = CreateWindow(L"EDIT", NULL, WS_CHILD | WS_VISIBLE | WS_VSCROLL | ES_MULTILINE | ES_WANTRETURN,
            0, 0, 0, 0, hwnd, NULL, GetModuleHandle(NULL), NULL);
        break;
    }
    case WM_SIZE: {
        // Resize edit control to fill client area
        RECT rc;
        GetClientRect(hwnd, &rc);
        MoveWindow(hwndEdit, 0, 0, rc.right, rc.bottom, TRUE);
        break;
    }
    case WM_COMMAND:
        switch (LOWORD(wParam)) {
        case IDM_SAVE:
            SaveFile(hwndEdit, hwnd);
            break;
        case IDM_LOAD:
            LoadFile(hwndEdit, hwnd);
            break;
        }
        break;
    case WM_DESTROY:
        PostQuitMessage(0);
        break;
    default:
        return DefWindowProc(hwnd, msg, wParam, lParam);
    }
    return 0;
}

void SaveFile(HWND hwndEdit, HWND hwnd) {
    if (wcslen(filename) > 0) {
        // Save to existing filename
        int length = GetWindowTextLength(hwndEdit);
        std::wstring content(length + 1, L'\0');
        GetWindowText(hwndEdit, &content[0], length + 1);
        HANDLE hFile = CreateFile(filename, GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
        WriteFile(hFile, content.c_str(), content.size() * sizeof(WCHAR), NULL, NULL);
        CloseHandle(hFile);
    }
    else {
        // Open save dialog
        OPENFILENAME ofn = { 0 };
        ofn.lStructSize = sizeof(ofn);
        ofn.hwndOwner = hwnd;
        ofn.lpstrFile = filename;
        ofn.nMaxFile = MAX_PATH;
        ofn.lpstrFilter = L"Text Files (*.txt)\0*.txt\0All Files (*.*)\0*.*\0";
        ofn.Flags = OFN_OVERWRITEPROMPT;
        if (GetSaveFileName(&ofn)) {
            SaveFile(hwndEdit, hwnd); // Recursive call with new filename
        }
    }
}

void LoadFile(HWND hwndEdit, HWND hwnd) {
    OPENFILENAME ofn = { 0 };
    ofn.lStructSize = sizeof(ofn);
    ofn.hwndOwner = hwnd;
    ofn.lpstrFile = filename;
    ofn.nMaxFile = MAX_PATH;
    ofn.lpstrFilter = L"Text Files (*.txt)\0*.txt\0All Files (*.*)\0*.*\0";
    ofn.Flags = OFN_FILEMUSTEXIST;
    if (GetOpenFileName(&ofn)) {
        HANDLE hFile = CreateFile(filename, GENERIC_READ, 0, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
        DWORD size = GetFileSize(hFile, NULL);
        std::wstring content(size / sizeof(WCHAR) + 1, L'\0');
        ReadFile(hFile, &content[0], size, NULL, NULL);
        CloseHandle(hFile);
        SetWindowText(hwndEdit, content.c_str());
    }
}