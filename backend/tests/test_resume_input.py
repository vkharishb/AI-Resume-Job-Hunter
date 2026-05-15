from app.services.resume_input import github_to_raw_url


def test_github_blob_url_converts_to_raw():
    url = "https://github.com/user/repo/blob/main/resume.pdf"

    assert github_to_raw_url(url) == "https://raw.githubusercontent.com/user/repo/main/resume.pdf"
