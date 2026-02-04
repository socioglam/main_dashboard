import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import AuthError

# Replace with the token you generated in Step 3
ACCESS_TOKEN = "sl.u.AGQzG-CFUL3Q35qq1vCjM8gVDcRHfXQzhjPJ-lmJKVZ1P9BYUTAILm3G6EB7OOZzhN6bMHuDmsOQBSP0pX_fZABQ4zoR4_fRuYLrjgutW1-StHew8yHYDj5AQG11cJmQBB8St3ICEo65oCXc78tBkp7uoCMeAGrG0Sfkbh500N6Y-cnYoM3-uCNTQDsDAit40O48Oqbh17S_9CK0_QsGpoObBURy_zywTSwfFTAmIX4Sk745dAZ7IU1zmZguFHkiMObM01qGnH4j7dio2XNbsQUCvtQkw5mw-dQ_vL9k6-kK4nbFnMSXL87zy_AwVEkbBfn7XMckWAdQRTa-yPe1V8txBMaC9KYQme0J0dB-MVVbVg4Yuk98VxfbB8otMZs4ugNXMv9NiLkzvnl7OCdCNp12zEavgMn0rKruCu8PN_7i8sPkxEODuBd1YEtDrfsXXiu4QjM_Aw9k6-GxuOCLfCQFZrgPIowEvLf1EcaEs85I7ND63oLkV64YBy09nZyNx3feJVHP1cGDpCEjSVDfFlgNlkODy71reGneDrWMc_ThvQ9cc3G9XvUDtbFysZBun2EKuUQMVGFRuXsSxPyXDsMauAS_9-lJmlBIBgSUZ2jlX44SaMmOYaNcW2R15wjm0zJs-7ssQZLR6tZFnwnKK1JlhuZjyOzlGfsBAi0y0GIoEd-UvX7r9q9VcAmYUrbeReXCnvLsl9H4tK9WmVm74JAPu7R5Nkwkfm5MmjXO8B5O-St3cM97G3R3bFjtS8CtjTHHl-Mv8euTfU0eFWOIZi8EkuD_MtPAPPp0-Qyd6aKZaVSBsnEgXsH-Sw9a1EkgGl01oUhANkuVhUSQG2_IUPMp9LUuGuWhHIhwoyCSG8SKma4k807mnhEVabokQ1bdOsb_IfX56yYyhktYeQXr7nibDKVHeQbRiNGkaQAFbPoYVVEEgzOe-N3Hs8l5OSeLKVjM86CLeeDTg6Vc6wC8HcOuvl4DwQXk6aC8GRfiCUrpk6CmqyI-_uPowBMRPtFO-JiIGK0x2HJKwtBFfQ_prS0E9akX-7K8jODsvMeKqoQfwGgurMB8laUWPGn9GzCeDJ69AsOFrXBjDsGi53e6czuuAFxVYxczZH8L5NC_zWhj3PGv9s0dDfG-vHZbrVlHwVZX71V59Mid4iaRBfmrYM9eIvpOHOC_2_RRBEJGK_uqtJkRPhtbIBHTGJGqVQgWkd-QE-ZZp2Lb4-6dx0SKtvcDmHA4i-4HzcR9ouQvrNyS7D-XLxGBFfxOWBvXgVVE3IR2n3cYn8axLx1oRBVFnRoIuyPPDFN7GjYx0yDy2Pe1Ivh9ZQoe_VYqv5q7bFt07-QT363kYmUib7Q5U6Vu9im1w0_wYdlZKCRUeIJzdWW2oQTBjSH3P0ZYAdfe4x3T-dkXhPiBUQDdtQ6y98puWt9pmLOyCF9fILbvS5c2CVLmwg"


def test_upload():
    # 1. Create the client
    dbx = dropbox.Dropbox(ACCESS_TOKEN)

    # 2. Check connection
    try:
        user = dbx.users_get_current_account()
        print(f"Connected to account: {user.name.display_name}")
    except AuthError:
        print("Error: Invalid Access Token")
        return

    # 3. Upload a test file
    # Note: If you selected 'App folder' access, this path is relative to that folder.
    file_content = b"Hello! This is a test from the Dropbox API."
    upload_path = "/test_upload.txt"

    try:
        dbx.files_upload(file_content, upload_path, mode=WriteMode("overwrite"))
        print(f"Success! File uploaded to {upload_path}")
    except Exception as e:
        print(f"Upload failed: {e}")


if __name__ == "__main__":
    test_upload()
