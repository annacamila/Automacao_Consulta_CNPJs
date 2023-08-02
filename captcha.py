from anticaptchaofficial.imagecaptcha import imagecaptcha


def resolver_captcha_imagem(caminho_imagem_captcha: str) -> dict[str]:
    solver = imagecaptcha()
    solver.set_verbose(1)
    solver.set_key('sua_senha_anticaptcha')
    resultado_solucao = solver.solve_and_return_solution(caminho_imagem_captcha)
    if resultado_solucao != 0:
        print(resultado_solucao)
        resposta_captcha = {'code': resultado_solucao, 'task_id': solver.task_id}
        return resposta_captcha
    else:
        raise Exception(f'Erro ao tentar resolver captcha de imagem pelo antiCaptcha - {solver.error_code} - {solver.err_string}')
    
