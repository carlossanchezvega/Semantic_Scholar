from re import search




def main():
    url = "https://www.semanticscholar.org/paper/Identifying-Relations-for-Open-Information-Fader-Soderland/0796f6cd7f0403a854d67d525e9b32af3b277331"
    value = search('https://www.semanticscholar.org/paper/(.+)/', url)
    if value is not None:
        value = value.group(1) if len(value.group(1))< 256 == value.group(1) else value.group(1)[0:254]
        print(value)

if __name__ == '__main__':
    # sys.exit(main(sys.argv)) # used to give a better look to exists
    main()

