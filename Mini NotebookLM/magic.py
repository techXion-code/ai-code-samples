from rembg import remove; open("out.png","wb").write(remove(open("input.png","rb").read()))
