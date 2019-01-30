import attr
import time
from navmazing import NavigateToAttribute, NavigateToSibling
from wait_for import wait_for
import pytest
from selenium.common.exceptions import NoSuchElementException

from usmqe.base.application.entities import BaseCollection, BaseEntity
from usmqe.base.application.views.cluster import ClustersView, UnmanageConfirmationView
from usmqe.base.application.views.cluster import UnmanageTaskSubmittedView
from usmqe.base.application.views.host import ClusterHostsView
from usmqe.base.application.views.volume import ClusterVolumesView
from usmqe.base.application.views.task import ClusterTasksView
from usmqe.base.application.views.event import ClusterEventsView
from usmqe.base.application.views.importcluster import ImportClusterView, ImportTaskSubmittedView
from usmqe.base.application.implementations.web_ui import TendrlNavigateStep, ViaWebUI
from usmqe.base.application.entities.hosts import HostsCollection
from usmqe.base.application.entities.volumes import VolumesCollection
from usmqe.base.application.entities.tasks import TasksCollection
from usmqe.base.application.entities.events import EventsCollection
from usmqe.base.application.views.grafana import GrafanaClusterDashboard


LOGGER = pytest.get_logger('clusters', module=True)


@attr.s
class Cluster(BaseEntity):
    cluster_id = attr.ib()
    name = attr.ib()
    health = attr.ib()
    version = attr.ib()
    managed = attr.ib()
    hosts_number = attr.ib()
    status = attr.ib()
    # attributes below are not defined until cluster is imported
    volumes_number = attr.ib()
    alerts = attr.ib()
    profiling = attr.ib()

    _collections = {'hosts': HostsCollection,
                    'volumes': VolumesCollection,
                    'tasks': TasksCollection,
                    'events': EventsCollection}

    @property
    def hosts(self):
        return self.collections.hosts

    @property
    def volumes(self):
        return self.collections.volumes

    @property
    def tasks(self):
        return self.collections.tasks

    @property
    def events(self):
        return self.collections.events

    def update(self):
        view = self.application.web_ui.create_view(ClustersView)
        self.version = view.clusters(self.name).cluster_version.text
        self.managed = view.clusters(self.name).managed.text
        self.hosts_number = view.clusters(self.name).hosts.text
        self.status = view.clusters(self.name).status.text
        self.health = view.clusters(self.name).health
        if self.managed == "Yes":
            self.volumes_number = view.clusters(self.name).volumes.text
            self.alerts = view.clusters(self.name).alerts.text
            self.profiling = view.clusters(self.name).profiling.text
        else:
            self.volumes_number = None
            self.alerts = None
            self.profiling = None

    def cluster_import(self, cluster_name=None, profiling="enable"):
        """
        Cluster import function.
        Valid cluster name contains only alphanumeric and underscore characters.
        Possible profiling values are "enable", "disable" or "leaveAsIs".
        """
        view = ViaWebUI.navigate_to(self, "Import")
        if cluster_name is not None:
            view.fill({"cluster_name": cluster_name,
                       "profiling": profiling})
            self.name = cluster_name
        else:
            view.fill({"profiling": profiling})
        view.confirm_import.click()
        time.sleep(1)
        view = self.application.web_ui.create_view(ImportTaskSubmittedView)
        time.sleep(2)
        view.close_button.click()
        time.sleep(60)
        for _ in range(40):
            self.update()
            if self.managed == "Yes":
                break
            else:
                time.sleep(5)
        LOGGER.debug("Cluster is managed: {}".format(self.managed))
        pytest.check(self.managed == "Yes")
        LOGGER.debug("Cluster status: {}".format(self.status))
        pytest.check(self.status == "Ready to Use")

    def unmanage(self, cancel=False, original_id=None):
        if original_id is not None:
            self.cluster_id = original_id
        view = self.application.web_ui.create_view(ClustersView)
        view.clusters(self.name).actions.select("Unmanage")
        view = self.application.web_ui.create_view(UnmanageConfirmationView)
        wait_for(lambda: view.is_displayed, timeout=3)
        view.unmanage.click()
        time.sleep(5)
        view = self.application.web_ui.create_view(UnmanageTaskSubmittedView)
        time.sleep(2)
        view.close()
        time.sleep(60)
        for _ in range(40):
            try:
                self.update()
                if self.managed == "No" and self.status == "Ready to Import":
                    break
                else:
                    time.sleep(5)
            except NoSuchElementException:
                if self.cluster_id != self.name:
                    self.name = self.cluster_id
                time.sleep(5)
        LOGGER.debug("Cluster is managed: {}".format(self.managed))
        pytest.check(self.managed == "No")
        LOGGER.debug("Cluster status: {}".format(self.status))
        pytest.check(self.status == "Ready to Import")

    def enable_profiling(self, cancel=False):
        view = self.application.web_ui.create_view(ClustersView)
        view.clusters(self.name).actions.select("Enable Profiling")
        time.sleep(40)
        for _ in range(40):
            self.update()
            if self.profiling == "Enabled":
                break
            else:
                time.sleep(5)
        LOGGER.debug("Cluster profiling value: {}".format(self.profiling))
        pytest.check(self.profiling == "Enabled")

    def disable_profiling(self, cancel=False):
        view = self.application.web_ui.create_view(ClustersView)
        view.clusters(self.name).actions.select("Disable Profiling")
        time.sleep(40)
        for _ in range(40):
            self.update()
            if self.profiling == "Disabled":
                break
            else:
                time.sleep(5)
        LOGGER.debug("Cluster profiling value: {}".format(self.profiling))
        pytest.check(self.profiling == "Disabled")

    def check_dashboard(self):
        view = ViaWebUI.navigate_to(self, "Dashboard")
        time.sleep(3)
        pytest.check(view.cluster_name.text == self.name)
        LOGGER.debug("Cluster name in grafana: {}".format(view.cluster_name.text))
        LOGGER.debug("Cluster name in main UI: {}".format(self.name))
        pytest.check(view.hosts_total.text.split(" ")[-1] == self.hosts_number)
        LOGGER.debug("Hosts in grafana: '{}'".format(view.hosts_total.text.split(" ")[-1]))
        LOGGER.debug("Hosts in main UI: '{}'".format(self.hosts_number))
        pytest.check(view.volumes_total.text.split(" ")[-1] == self.volumes_number)
        LOGGER.debug("Volumes in grafana: {}".format(view.volumes_total.text.split(" ")[-1]))
        LOGGER.debug("Volumes in main UI: {}".format(self.volumes_number))
        pytest.check(view.cluster_health.text == self.health)
        LOGGER.debug("Cluster health in grafana: '{}'".format(view.cluster_health.text))
        LOGGER.debug("Cluster health in main UI: '{}'".format(self.health))
        view.browser.selenium.close()
        view.browser.selenium.switch_to.window(view.browser.selenium.window_handles[0])

    def expand(self, cancel=False):
        pass

    @property
    def exists(self):
        pass


@attr.s
class ClustersCollection(BaseCollection):
    ENTITY = Cluster

    def get_all_cluster_ids(self):
        view = self.application.web_ui.create_view(ClustersView)
        return view.all_ids

    def get_clusters(self):
        view = ViaWebUI.navigate_to(self, "All")
        clusters_list = []
        for cluster_id in self.get_all_cluster_ids():
            if view.clusters(cluster_id).managed.text == "No":
                cluster = self.instantiate(
                    cluster_id,
                    cluster_id,
                    view.clusters(cluster_id).health,
                    view.clusters(cluster_id).cluster_version.text,
                    view.clusters(cluster_id).managed.text,
                    view.clusters(cluster_id).hosts.text,
                    view.clusters(cluster_id).status.text,
                    None,
                    None,
                    None)
                clusters_list.append(cluster)
            else:
                cluster = self.instantiate(
                    cluster_id,
                    cluster_id,
                    view.clusters(cluster_id).health,
                    view.clusters(cluster_id).cluster_version.text,
                    view.clusters(cluster_id).managed.text,
                    view.clusters(cluster_id).hosts.text,
                    view.clusters(cluster_id).status.text,
                    view.clusters(cluster_id).volumes.text,
                    view.clusters(cluster_id).alerts.text,
                    view.clusters(cluster_id).profiling.text)
                clusters_list.append(cluster)
        return clusters_list


@ViaWebUI.register_destination_for(ClustersCollection, "All")
class ClustersAll(TendrlNavigateStep):
    VIEW = ClustersView
    prerequisite = NavigateToAttribute("application.web_ui", "LoggedIn")

    def step(self):
        time.sleep(1)
        self.parent.navbar.clusters.select_by_visible_text("All Clusters")
        time.sleep(2)


@ViaWebUI.register_destination_for(Cluster, "Import")
class ClusterImport(TendrlNavigateStep):
    VIEW = ImportClusterView
    prerequisite = NavigateToAttribute("parent", "All")

    def step(self):
        time.sleep(1)
        self.parent.clusters(self.obj.name).import_button.click()


@ViaWebUI.register_destination_for(Cluster, "Hosts")
class ClusterHosts(TendrlNavigateStep):
    VIEW = ClusterHostsView
    prerequisite = NavigateToAttribute("parent", "All")

    def step(self):
        time.sleep(1)
        self.parent.navbar.clusters.select_by_visible_text(self.obj.name)
        time.sleep(2)


@ViaWebUI.register_destination_for(Cluster, "Volumes")
class ClusterVolumes(TendrlNavigateStep):
    VIEW = ClusterVolumesView
    prerequisite = NavigateToSibling("Hosts")

    def step(self):
        time.sleep(1)
        self.parent.vertical_navbar.volumes.click()


@ViaWebUI.register_destination_for(Cluster, "Tasks")
class ClusterTasks(TendrlNavigateStep):
    VIEW = ClusterTasksView
    prerequisite = NavigateToSibling("Hosts")

    def step(self):
        time.sleep(1)
        self.parent.vertical_navbar.tasks.click()


@ViaWebUI.register_destination_for(Cluster, "Events")
class ClusterEvents(TendrlNavigateStep):
    VIEW = ClusterEventsView
    prerequisite = NavigateToSibling("Hosts")

    def step(self):
        time.sleep(1)
        self.parent.vertical_navbar.events.click()


@ViaWebUI.register_destination_for(Cluster, "Dashboard")
class ClusterDashboard(TendrlNavigateStep):
    VIEW = GrafanaClusterDashboard
    prerequisite = NavigateToAttribute("parent", "All")

    def step(self):
        time.sleep(1)
        self.parent.clusters(self.obj.name).dashboard_button.click()
        time.sleep(1)
        self.view.browser.selenium.switch_to.window(self.view.browser.selenium.window_handles[1])
        time.sleep(1)
