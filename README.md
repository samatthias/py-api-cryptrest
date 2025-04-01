# py-api-cryptrest
A REST API written in Python with FASTAPI to encrypt and decrypt files with gpg. Later I may add linux age. GPG uses AES256 symetric encryption.


## Encryption parameters according to post:
https://crypto.stackexchange.com/questions/66318/how-secure-is-gpg-command-using-symmetric-aes-256-from-being-cracked

## Encryption command
gpg --symmetric --batch --passphrase <password> --s2k-mode 3 --s2k-count 65011712 --s2k-digest-algo SHA512 --s2k-cipher-algo AES256 --output <output file> <input file>

## Decryption command
gpg --decrypt --batch --passphrase asdf --output decrypted.pdf o2-1111_enc.enc

## Other sources:
https://www.nas.nasa.gov/hecc/support/kb/using-gpg-to-encrypt-your-data_242.html
https://nordpass.com/blog/xchacha20-encryption-vs-aes-256/
https://github.com/FiloSottile/age




## Curl encrypt example
curl.exe -v http://127.0.0.1:8080/encrypt -H "Content-Type: multipart/form-data" -F "password=asdf" -F "outputFilename=0001.pdf.enc" -F "file=@0001.pdf" -o 0001.pdf.enc

## Curl decrypt example
curl.exe -v http://127.0.0.1:8080/decrypt -H "Content-Type: multipart/form-data" -F "password=asdf" -F "outputFilename=0001-encrypted.pdf" -F "file=@0001.pdf.enc" -o 0001-encrypted.pdf

## build container
podman build -t py-api-cryptrest:yyyy-mm-dd -f .\build\Dockerfile .

## run container
podman run podman run -it -p 8080:8080 -d localhost/py-api-cryptrest:yyyy-mm-dd

