class Header extends HTMLElement {
    connectedCallback() {
      this.innerHTML = `
      <div class="row" style="margin-bottom: 20px;">
          <nav class="navbar navbar-expand-lg navbar-light bg-light">
              <a class="navbar-brand" href="#"></a>
              <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
              </button>
              <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                  <li class="nav-item ">
                    <a class="nav-link" href="#">Profile <span class="sr-only">(current)</span></a>
                  </li>
                  <li class="nav-item active">
                    <a class="nav-link" href="#">Evaluation1</a>
                  </li>
                  <li class="nav-item">
                    <a class="nav-link" href="#">Evaluation2</a>
                  </li>
                  <li class="nav-item">
                    <a class="nav-link disabled" href="#">Aide</a>
                  </li>
                </ul>
              </div>
            </nav>
      </div>`
    }
  }
  class Footer extends HTMLElement {
    connectedCallback() {
      this.innerHTML = `    
      <div class="row">
            <footer class="container text-center text-lg-start bg-light text-muted" style="border-radius: 20px; margin-top: 20px;">
            <!-- Section: Social media -->
            <section
              class="d-flex justify-content-center justify-content-lg-between p-4 border-bottom"
            >
      
          
              <!-- Right -->
              <div>
                <a href="" class="me-4 text-reset">
                  <i class="fab fa-facebook-f"></i>
                </a>
                <a href="" class="me-4 text-reset">
                  <i class="fab fa-twitter"></i>
                </a>
                <a href="" class="me-4 text-reset">
                  <i class="fab fa-google"></i>
                </a>
                <a href="" class="me-4 text-reset">
                  <i class="fab fa-instagram"></i>
                </a>
                <a href="" class="me-4 text-reset">
                  <i class="fab fa-linkedin"></i>
                </a>
                <a href="" class="me-4 text-reset">
                  <i class="fab fa-github"></i>
                </a>
              </div>
              <!-- Right -->
            </section>
            <!-- Section: Social media -->
          
            <!-- Section: Links  -->
            <section class="">
              <div class="container text-center text-md-start mt-5">
                <!-- Grid row -->
                <div class="row mt-3">
                  <!-- Grid column -->
                  <div class="col-md-3 col-lg-4 col-xl-3 mx-auto mb-4">
                    <!-- Content -->
                    <h6 class="text-uppercase fw-bold mb-4">
                      <i class="fas fa-gem me-3"></i>Lorem 
                    </h6>
                    <p>
                       Lorem ipsum dolor sit amet, consectetur adipisicing elit.
                    </p>
                  </div>
                  <!-- Grid column -->
          
                  
                  <!-- Grid column -->
          
                  <!-- Grid column -->
                  <div class="col-md-3 col-lg-2 col-xl-2 mx-auto mb-4">
                    <!-- Links -->
                    <h6 class="text-uppercase fw-bold mb-4">
                      Liens Utiles
                    </h6>
                    <p>
                      <a href="#!" class="text-reset">Aide</a>
                    </p>
                  </div>
                  <!-- Grid column -->
          
                  <!-- Grid column -->
                  <div class="col-md-4 col-lg-3 col-xl-3 mx-auto mb-md-0 mb-4">
                    <!-- Links -->
                    <h6 class="text-uppercase fw-bold mb-4">
                      Contact
                    </h6>
                    <p><i class="fas fa-home me-3"></i> Adresse , ALG</p>
                    <p>
                      <i class="fas fa-envelope me-3"></i>
                      info@example.com
                    </p>
                    <p><i class="fas fa-phone me-3"></i> + 00 000 00 00C</p>
                  </div>
                  <!-- Grid column -->
                </div>
                <!-- Grid row -->
              </div>
            </section>
            <!-- Section: Links  -->
          
            <!-- Copyright -->
            <div class="text-center p-4" style="background-color: rgba(0, 0, 0, 0.05);">
              © 2022 Copyright:
              <a class="text-reset fw-bold" href=#>site.com</a>
            </div>
            <!-- Copyright -->
          </footer>
      
          </div>
      `;
    }
  }

customElements.define('main-header', Header);
customElements.define('main-footer', Footer);

