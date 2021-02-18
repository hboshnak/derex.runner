describe("course navigator", () => {
  it(` User logged in be able to switch between "Wiki, Progrss, Instructor, Discussion" courses tabs of a course already enrolled in `, function() {
    cy.login(Cypress.env("user_email"), Cypress.env("user_password"));
    cy.visit("/");

    cy.get("body").find("ul.courses-listing").then(res => {
      if (res[0].children.length > 0) {
        cy.get(res[0].children[0]).then($button => {
          cy.wrap($button).click();
        });
        // move to Description tab
        cy.get('strong').then($button => {
          cy.wrap($button).click();
        });

        // move to Progrss tab
        cy.get("#content > .navbar > .navbar-nav > :nth-child(2) > .nav-link").then($button => {
          cy.wrap($button).click();
        });
        // move to Instructor tab
        cy.get(".tabs > :nth-child(3) > a").then($button => {
          cy.wrap($button).click();
        });
        // move to Discussion tab
        cy.get(".tabs > :nth-child(4) > a").then($button => {
          cy.wrap($button).click();
        });
      } else {
        console.log("No Courses");
      }
    });
  });
});