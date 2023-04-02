ASUS RT-AX92U overflow

Firmware version - 3.0.0.4.386_45898

When AiCloud 2.0 Cloud Disk functionality is enabled, the router start lighttpd server on port 443.
There is a heap overflow when parsing GETTHUMBIMAGE HTTP request.

Consider the following code from mod_webdav.c:

```
static int get_thumb_image(char* path, plugin_data *p, char **out){
        UNUSED(p);
        
        if(is_dms_enabled()==0){
                return 0;
        }
        
        char* thumb_dir = (char *)malloc(PATH_MAX);
        if(!thumb_dir) return 0;

        if (buffer_is_empty(p->minidlna_db_dir))
                get_minidlna_db_path(p);
        
        strcpy(thumb_dir, p->minidlna_db_dir->ptr);
        strcat(thumb_dir, "/art_cache/tmp");
        
        char* filename = NULL;  
        extract_filename(path, &filename);
        const char *dot = strrchr(filename, '.');
        int len = dot - filename;
        
        char* filepath = NULL;
        extract_filepath(path, &filepath);
                                        
        strcat(thumb_dir, filepath);
        strncat(thumb_dir, filename, len);
        strcat(thumb_dir, ".jpg");
		...
}
```

The variable 'path' comes from http request, there is no size limit.

Note that the real code slightly differs from the source, lighttpd allocates 0x1000 for variable thumb_dir.

```
How to verify:
1) insert usb media
2) enable Cloud Disk (AiCloud 2.0 -> Cloud Disk)
3) run t1.py
```
