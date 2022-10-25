#include <string>
#include <iostream>
#include <cstdint>
#include <cstring>
#pragma once
using namespace std;
extern "C"
{
	void cipher(const char* msg, const char* key, char* buffer, int msg_len, int key_len);
}
void cipher(const char *msg, const char *key, char *buffer, int msg_len, int key_len)
{
    for (unsigned i = 0; i < msg_len; i++)
        buffer[i] = (msg[i] ^ key[i % key_len]);
}
