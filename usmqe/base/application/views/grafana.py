from widgetastic.widget import Text, View


class BaseGrafanaDashboard(View):
    dashboard_name = Text(".//a[@class='navbar-page-btn']")
    cluster_name = Text(".//label[contains(text(), 'Cluster Name')]"
                        "/parent::div/value-select-dropdown")


class GrafanaClusterDashboard(BaseGrafanaDashboard):
    cluster_health = Text(".//span[text() = 'Health']/ancestor::div[@class='panel-container']"
                          "/descendant::span[@class='singlestat-panel-value']")
    hosts_total = Text(".//h1/a[contains(text(), 'Hosts')]/ancestor::div[@class='bottom_section']"
                       "/descendant::span[text() = 'Total']/following-sibling::span")
    volumes_total = Text(".//h1/a[contains(text(), 'Volumes')]/ancestor::div[@class="
                         "'bottom_section']/descendant::span[text() = 'Total']"
                         "/following-sibling::span")

    @property
    def is_displayed(self):
        return self.dashboard_name.text.find("Cluster") >= 0


class GrafanaHostDashboard(BaseGrafanaDashboard):
    # in hostnames all dots are replaced with underscores
    host_name = Text(".//label[contains(text(), 'Host Name')]/parent::div/value-select-dropdown")
    host_health = Text(".//span[text() = 'Health']/ancestor::div[@class='panel-container']"
                       "/descendant::span[@class='singlestat-panel-value']")
    # brick total looks like " - 5" instead of "5"
    bricks_total = Text(".//span[text() = 'Total']/following-sibling::span")

    @property
    def is_displayed(self):
        return self.dashboard_name.text.find("Host") >= 0


class GrafanaVolumeDashboard(BaseGrafanaDashboard):
    pass


class GrafanaBrickDashboard(BaseGrafanaDashboard):
    pass
